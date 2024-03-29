#!/usr/bin/env python3
from planeacion_a import inicio_fin
import rospy
import time
import threading
from std_msgs.msg import Header
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray


class Poses_Publish(object):
	def __init__(self):
		super(Poses_Publish, self).__init__()
		
		self.opciones = True
		
		self.glo_x,self.glo_y,self.glo_z = 0.0,0.0,0.0
		self.ini_pose = [self.glo_x,self.glo_y,self.glo_z]
		self.end_pose = [self.glo_x,self.glo_y,self.glo_z]

		self.landmarks= [[7.31, 0], [7.19,7.55], [18.85,-3.59], [33.77,6.41], [13.22,-13.61],[21.01,13.21],[20.96,3.36], [20.40, -19.41], [14.77,6.89],[22.46,-10.36], [31.56, -18.81], [29.92,11.44], [32.79,-6.79], [2.04,-12.02], [7.63,13.24]]
		self.waypoints=[[12.19,8.73],[25.04,4.36],[28.62,-6.17],[11.63,-16.85],[7.64,-5.55],[27.48,-13.65]]
		print('Starting robocol_poses node...')
		rospy.init_node('robocol_poses')
		# Publishers
		print('Publishing in /Robocol/Inicio_fin (PoseArray)')
		self.pubPose = rospy.Publisher('/Robocol/Inicio_fin',PoseArray,queue_size=1)
		# print('Publishing in /robocol/odom (Odometry)\n')
		# self.pubOdom = rospy.Publisher('/robocol/odom',Odometry, queue_size=1)
		# # Subscribers
		print('Subscribing in zed2/odom (Odometry)\n')
		
		rospy.Subscriber('zed2/odom',Odometry, self.odometry_callback)
		# print('Subscribing to /zed2/imu/data (Imu)')
		# rospy.Subscriber('/zed2/imu/data', Imu, self.imu_callback)
		# print('Subscribing to /robocol/vision_correction (Twist)')
		# rospy.Subscriber('/robocol/vision_correction', Twist, self.vision_correction_callback)
		rospy.on_shutdown(self.kill)
		print('')
		x = threading.Thread(target=self.thread_function)
		x.start()

	def odometry_callback(self,param):
		self.glo_x = param.pose.pose.position.x
		self.glo_y = param.pose.pose.position.y
		self.glo_z = param.pose.pose.position.z
		self.ini_pose = [self.glo_x,self.glo_y,self.glo_z]

	def thread_function(self):
		while self.opciones:
			print("Choose an option:")
			print(" W: To choose Waypoint")
			print(" C: To send new coordinate.")
			print(" R: To publish last coordinate again.")
			op = str(input(' > '))
			print(op)
			if op == "W":
				print(' WAYPOINTS:')
				for i in range(len(self.waypoints)):
					msg = '  Landmark {:2d} -->   x: {:6.2f}   y: {:6.2f}'
					print(msg.format(i+1,self.waypoints[i][0],self.waypoints[i][1]))
				print('   Choose a landmark:')
				lm = float(input('   > '))
				try:
					self.x2 = self.waypoints[int(lm)-1][0]
					self.y2 = self.waypoints[int(lm)-1][1]
					print(msg.format(int(lm),xlm,ylm))
					self.pub_coords(self.glo_x,self.x2,self.glo_y,self.y2)
				except Exception as e:
					print('Not a number')
			elif op == "C":
				print(" Enter desired coordinates:")
				print("  Enter x coordinate:")
				self.x2 = float(input('  > '))
				print("  Enter y coordinate:")
				self.y2 = float(input('  > '))
				self.pub_coords(self.glo_x,self.x2,self.glo_y,self.y2 )
			elif op == "R":
				self.pub_coords(self.glo_x,self.x2,self.glo_y,self.y2)
			else:
				print(' COMMAND NOT RECOGNIZED.')
			print('')
		print('Closing thread...')

	def kill(self):
		print("\nKilling node...")
		self.opciones = False
		print('Press Enter to end...')
		
	def pub_coords(self,x1,x2,y1,y2):
		poses = []
		ini_fin = PoseArray()
		inicio = Pose() 
		fin = Pose()
		inicio.position.x = x1
		inicio.position.y = y1
		fin.position.x = x2
		fin.position.y = y2
		poses.append (inicio)
		poses.append (fin)
		print(' Sending:')
		print('  Initial pose: ')
		print('   x: {}  y: {} '.format(x1,y1))
		print('  Final pose: ')
		print('   x: {}  y: {}  '.format(x2,y2))
		ini_fin.poses = poses
		self.pubPose.publish(ini_fin)

	def pub_test(self):
		print('Printing test')
		test = Float32MultiArray()
		self.pubPose.publish(test)

def main():
	try:
		poses_Publish = Poses_Publish()

		time.sleep(1)
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			# poses_Publish.pub_test()
			rate.sleep()
	except rospy.ROSInterruptException:
		return
	except KeyboardInterrupt:
		return

if __name__ == '__main__':
	main()
