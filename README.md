[//]: # (Image References)

[image1]: ./assets/mogi_bot_camera_1.png "Camera"
[image2]: ./assets/mogi_bot_camera_2.png "Camera"
[image3]: ./assets/mogi_bot_camera_3.png "Camera"
[image4]: ./assets/mogi_bot_camera_4.png "Camera"
[image5]: ./assets/mogi_bot_imu_1.png "IMU"
[image6]: ./assets/mogi_bot_imu_2.png "IMU"
[image7]: ./assets/mogi_bot_imu_3.png "IMU"
[image8]: ./assets/mogi_bot_camera_5.png "Camera" 
[image9]: ./assets/mogi_bot_camera_6.png "Camera" 
[image10]: ./assets/mogi_bot_camera_7.png "Camera" 
[image11]: ./assets/mogi_bot_camera_8.png "Camera" 
[image12]: ./assets/mogi_bot_camera_9.png "Camera" 
[image13]: ./assets/mogi_bot_gps_1.png "GPS"
[image14]: ./assets/mogi_bot_gps_2.png "GPS"
[image15]: ./assets/mogi_bot_gps_3.png "GPS"
[image16]: ./assets/mogi_bot_gps_4.png "GPS"
[image17]: ./assets/mogi_bot_gps_5.png "GPS"
[image18]: ./assets/mogi_bot_lidar_1.png "Lidar"
[image19]: ./assets/mogi_bot_lidar_2.png "Lidar"
[image20]: ./assets/mogi_bot_lidar_3.png "Lidar"
[image21]: ./assets/mogi_bot_lidar_4.png "Lidar"
[image22]: ./assets/mogi_bot_velodyne_1.png "Velodyne"
[image23]: ./assets/mogi_bot_velodyne_2.png "Velodyne"
[image24]: ./assets/mogi_bot_velodyne_3.png "Velodyne"
[image25]: ./assets/mogi_bot_rgbd_1.png "RGBD"
[image26]: ./assets/mogi_bot_rgbd_2.png "RGBD"
[image27]: ./assets/mogi_bot_rgbd_3.png "RGBD"
[image28]: ./assets/add_ball.png "Ball"
[image29]: ./assets/chase_ball_1.png "Ball"
[image30]: ./assets/chase_ball_2.png "Ball"
[image31]: ./assets/chase_ball_3.png "Ball"


# 5. - 6. hét - Szenzorok szimulációja Gazeboban

# Hova fogunk eljutni?

<a href="https://youtu.be/8bnjzPTNLfc"><img height="400" src="./assets/youtube1.png"></a>
<a href="https://youtu.be/-YCcQZmKJtY"><img height="400" src="./assets/youtube2.png"></a>

# Tartalomjegyzék
1. [Kezdőcsomag](#Kezdőcsomag)  
1.1. [A tree parancs](#A-`tree`-parancs)
2. [Szenzorok 1](#Szenzorok-1)  
2.1. [Kamera](#Kamera)  
2.2. [IMU](#IMU)  
2.3. [GPS](#GPS)
3. [GPS waypoint követés](#GPS-waypoint-követés)
4. [Szenzorok 2](#Szenzorok-2)  
4.1. [Lidar](#Lidar)  
4.2. [Velodyne VLP16 lidar](#Velodyne-VLP16-lidar)  
4.3. [RGBD kamera](#RGBD-kamera)
5. [Képfeldolgozás ROS-ban OpenCV-vel](#Képfeldolgozás-ROS-ban-OpenCV-vel)

# Kezdőcsomag
A lecke kezdőcsomagja épít a Week-3-4-Gazebo-basics anyagára, de egy külön GIT repositoryból dolgozunk, így nem feltétele az előző `bme_gazebo_basics` csomag megléte.

A kiindulási projekt tartalmazza a Gazebo világ szimulációját, az alap differenciálhajtású MOGI robotunk modelljét és szimulációját, valamint az alap launchfájlokat és RViz fájlokat.

A kezdőprojekt letöltése:
```console
git clone -b starter-branch https://github.com/MOGI-ROS/Week-5-6-Gazebo-sensors.git
```

## A `tree` parancs
A kezdőprojekt tartalma a következő:
```console
david@DavidsLenovoX1:~/bme_catkin_ws/src/Week-5-6-Gazebo-sensors/bme_gazebo_sensors$ tree
.
├── CMakeLists.txt
├── launch
│   ├── check_urdf.launch
│   ├── spawn_robot.launch
│   ├── teleop.launch
│   └── world.launch
├── meshes
│   ├── lidar.dae
│   ├── mogi_bot.dae
│   ├── vlp16.dae
│   └── wheel.dae
├── package.xml
├── rviz
│   ├── check_urdf.rviz
│   └── mogi_world.rviz
├── urdf
│   ├── materials.xacro
│   ├── mogi_bot.gazebo
│   └── mogi_bot.xacro
└── worlds
    └── world_modified.world
```
A mappák tartalma egyszerűen listázható így a `tree` paranccsal, ha csak bizonyos mélységig szeretnétek listázni, akkor megtehetitek a `-L` kapcsoló segítségével. Például `tree -L 2`.

# Szenzorok 1
## Kamera
A kamera hozzáadása két lépésben történik, először adjuk hozzá a kamerát a robotunk URDF fájljához.
A kamera egy új link lesz `camera_link` néven, ami fixed joint-tal csatlakozik a robot alvázához. Az egyszerűség kedvéért, legyen a kameránk egy kis piros kocka.

### URDF
```xml
  <!-- Camera -->
  <joint type="fixed" name="camera_joint">
    <origin xyz="0.225 0 0.075" rpy="0 0 0"/>
    <child link="camera_link"/>
    <parent link="base_link"/>
    <axis xyz="0 1 0" />
  </joint>

  <link name='camera_link'>
    <pose>0 0 0 0 0 0</pose>
    <inertial>
      <mass value="0.1"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia
          ixx="1e-6" ixy="0" ixz="0"
          iyy="1e-6" iyz="0"
          izz="1e-6"
      />
    </inertial>

    <collision name='collision'>
      <origin xyz="0 0 0" rpy="0 0 0"/> 
      <geometry>
        <box size=".05 .05 .05"/>
      </geometry>
    </collision>

    <visual name='camera_link_visual'>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size=".05 .05 .05"/>
      </geometry>
    </visual>

  </link>

  <gazebo reference="camera_link">
    <material>Gazebo/Red</material>
  </gazebo>
```

A kamerákat használhatjuk ROS esetén a transzformációk megadása nélkül is, azonban ez a gyakorlatban nem praktikus, mert az RViz képes a megjelenített adatokat a transzformációknak megfelelően overlay-elni a kamera képére. Ez csak akkor működik, ha a kameránk transzformációját megadtuk (és helyesen adtuk meg) az URDF fájlban.

A Gazebo és az RViz kamera transzformációja között azonban van némi ellentmondás, és ha csak a fenti sorok szerepelnek az URDF-ben helytelen lesz a kamera képére vetített overlay.

Ezt egy újabb link, a `camera_link_optical` segítségével tudjuk orvosolni, ahol meg tudjuk oldani a további szükséges transzformációkat.
```xml
  <joint type="fixed" name="camera_optical_joint">
    <origin xyz="0 0 0" rpy="-1.5707 0 -1.5707"/>
    <child link="camera_link_optical"/>
    <parent link="camera_link"/>
  </joint>

  <link name="camera_link_optical">
  </link>
```

Nézzük meg a kameránk helyét a `check_urdf.launch` fájlunk segítségével:  
```console
roslaunch bme_gazebo_sensors check_urdf.launch
```
![alt text][image1]

A kameránk helyét ezzel a sorral tudjuk módosítani:
```xml
<origin xyz="0.225 0 0.075" rpy="0 0 0"/>
```

### Gazebo plugin

Ha elégedettek vagyunk a kamera helyzetével, hozzuk létre a Gazebo plugint is, ami a kameránk szimulációját csinálja:
```xml
  <!-- Camera -->
  <gazebo reference="camera_link">
    <sensor type="camera" name="camera1">
      <update_rate>30.0</update_rate>
      <visualize>false</visualize>
      <camera name="head">
        <horizontal_fov>1.3962634</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>
          <far>25.0</far>
        </clip>
        <noise>
          <type>gaussian</type>
          <!-- Noise is sampled independently per pixel on each frame.
               That pixel's noise value is added to each of its color
               channels, which at that point lie in the range [0,1]. -->
          <mean>0.0</mean>
          <stddev>0.007</stddev>
        </noise>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <alwaysOn>true</alwaysOn>
        <updateRate>0.0</updateRate>
        <cameraName>head_camera</cameraName>
        <imageTopicName>image_raw</imageTopicName>
        <cameraInfoTopicName>camera_info</cameraInfoTopicName>
        <frameName>camera_link_optical</frameName>
        <hackBaseline>0.07</hackBaseline>
        <distortionK1>0.0</distortionK1>
        <distortionK2>0.0</distortionK2>
        <distortionK3>0.0</distortionK3>
        <distortionT1>0.0</distortionT1>
        <distortionT2>0.0</distortionT2>
      </plugin>
    </sensor>
  </gazebo>
```

Indítsuk is el a kamerával felszerelt robotunk szimulációját:

```console
roslaunch bme_gazebo_sensors spawn_robot.launch
```

![alt text][image2]

![alt text][image3]

A kamera képére ráközelítve láthatjátok az overlay-t. Ez a későbbiekben, ahol több szenzort is adunk majd a robotunkhoz hasznosabb és látványosabb lesz.

![alt text][image4]

### Paraméterek 
A paraméter között természetesen tudjuk állítani a kamera felbontását és képfrissítési frekvenciáját, de ezeken felül van még néhány izgalmas paraméter is. Ilyen például a:
```xml
<visualize>true</visualize>
```
Ennek segítségével bekapcsolhatjuk a Gazeboban, hogy megjelenítse a szenzorunk által érzékelt adatokat. Ezt a későbbiekben több másik szenzoron is kipróbáljuk majd.


A látószöget a következő paraméter segítségével állíthatjuk:
```xml
<horizontal_fov>1.3962634</horizontal_fov>
```
A fenti képen egy szűkebb a lentin egy tágabb látószögű kamera képét látjátok.
![alt text][image9]
![alt text][image8]

Ezen felül a Gazeboval lehetséges a [Brown-Conrady féle lencsetorzítás modell](https://en.wikipedia.org/wiki/Distortion_(optics)) használata is. Ezeket a valós kameránk kalibrációjából tudjuk meghatározni. Részletes információ [itt](http://gazebosim.org/tutorials?tut=camera_distortion&cat=sensors) érhető el.

Az RViz után nézzük meg a kamera által küldött topic-okat rqt-ben is:
![alt text][image10]

A szimulált kamera alapértelmezetten a `/head_camera/image_raw` topicban küldi a kamera stream-et. Ezt a plugin beállításainál a következő paraméterekkel adtuk meg:
```xml
<cameraName>head_camera</cameraName>
<imageTopicName>image_raw</imageTopicName>
```

### Videótömörítés

ROS esetén a kamera alapértelmezetten az [image transport](http://wiki.ros.org/image_transport) csomag segjtségével küldi a tömörítetlen stream-et. Ez ennek megfelelően nagy sávszélességet is igényel. Ez egy mobil robot esetén ahol 1 vagy több kamera képét egy másik hálózati gépen is szeretnénk elérni nem elfogadható terhelés a hálózaton.

A megoldás a kamera stream tömörítése, ROS esetén szerencsére ehhez sem kell saját alkalmazást fejleszteni, ugyanis az image transport csomag kezel plugineket. ROS esetén a két legelterjedtebb plugin a [compressed image transport](http://wiki.ros.org/compressed_image_transport) valamint a [theora image transport](http://wiki.ros.org/theora_image_transport).

Ezeket a csomagokat csak egyszerűen telepítenünk kell és automatikusan megjelennek a tömörített képet tartalmazó topicok.
A compressed image transport konfigurálható jpg vagy png tömörítéssel, valamint a tömörítés mértékével.

De még ennél is szignifikánsan kisebb stream-et eredményez a [theora tömörítés](https://en.wikipedia.org/wiki/Theora), ami egy teljesen nyílt forrású és ingyenes videótömörítési eljárás.

És ezen felül a ROS-nak köszönhetően arra is van lehetőség, hogy a tömörítés paramétereit online változtassuk! Erre a ROS dynamic reconfigure toolját fogjuk használni, tegyünk is vele néhány próbát és közben figyeljük meg a sávszélesség adatokat rqt-ben!
```console
rosrun rqt_reconfigure rqt_reconfigure
```
![alt text][image11]

### Fisheye lencsék

A Gazebo camera pluginjével ezen kívül akár nagy látószögű kamerát is szimulálhatunk, ehhez a `wideanglecamera` type-ot kell választanunk, nagy field of view-t adunk, például 180 fok és meg kell adnunk a lencsét leíró függvényt a `lens` tagen belül az alábbi módon:
```xml
  <!-- Camera -->
  <gazebo reference="camera_link">
    <sensor type="wideanglecamera" name="camera1">
      <update_rate>30.0</update_rate>
      <visualize>false</visualize>
      <camera name="head">
        <horizontal_fov>3.141592</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>
          <far>25.0</far>
        </clip>
        <noise>
          <type>gaussian</type>
          <!-- Noise is sampled independently per pixel on each frame.
               That pixel's noise value is added to each of its color
               channels, which at that point lie in the range [0,1]. -->
          <mean>0.0</mean>
          <stddev>0.007</stddev>
        </noise>
        <lens>
          <type>custom</type> 
          <custom_function>
          <!-- manually defined mapping function r = c1*f*fun(theta/c2 + c3) More information here: https://en.wikipedia.org/wiki/Fisheye_lens#Mapping_function -->
            <c1>1.0</c1>    <!-- linear scaling -->
            <c2>1.95</c2>   <!-- angle scaling -->
            <f>6</f>        <!-- one more scaling parameter -->
            <fun>tan</fun>  <!-- one of sin,tan,id -->
          </custom_function>
          <!-- if it is set to `true` your horizontal FOV will remain as defined, othervise it depends on lens type and custom function, if there is one -->
          <scale_to_hfov>true</scale_to_hfov>  
          <!-- clip everything that is outside of this angle -->
          <cutoff_angle>2.84488668</cutoff_angle>
          <!-- resolution of the cubemap texture, the highter it is - the sharper is your image -->
          <env_texture_size>512</env_texture_size>
        </lens>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <alwaysOn>true</alwaysOn>
        <updateRate>0.0</updateRate>
        <cameraName>head_camera</cameraName>
        <imageTopicName>image_raw</imageTopicName>
        <cameraInfoTopicName>camera_info</cameraInfoTopicName>
        <frameName>camera_link_optical</frameName>
        <hackBaseline>0.07</hackBaseline>
        <distortionK1>0.0</distortionK1>
        <distortionK2>0.0</distortionK2>
        <distortionK3>0.0</distortionK3>
        <distortionT1>0.0</distortionT1>
        <distortionT2>0.0</distortionT2>
      </plugin>
    </sensor>
  </gazebo>
```
![alt text][image12]

## IMU

Az IMU az `Inertial Measurement Unit` rövidítése, és minimum egy 3 tengelyes MEMS gyorsulásmérőt és egy 3 tengelyes MEMS giroszkópot értünk alatta. Sokszor ez kiegészül egy 3 tengelyes magnetométerrel és akár egy barométerrel is. Az IMU nem helyettesíti egy robot egyéb szenzorjait (pl. odometria), viszont szenzorfúzió segítségével pontosíthatja a többi szenzor adatát.

IMU szimulációra több Gazebo plugin is létezik, én az alábbi Hector IMU controllert használom itt, ami a [Darmstadt-i egyetem](https://www.teamhector.de/) fejlesztése, és itt találjátok a ROS Wiki-n: http://wiki.ros.org/hector_gazebo_plugins.

A Linux csomagkezelőjével egyszerűen fel tudjátok tenni a Hector Gazebo pluginjeit:
```console
sudo apt install ros-noetic-hector-gazebo-plugins
```

Plusz olvasmánynak, egyéb IMU pluginekről és az összehasonlításukról szól ez a [diplomamunka](https://dspace.cvut.cz/bitstream/handle/10467/83404/F3-DP-2019-Cesenek-David-master_thesis_imu_modeling_cesenek_final-merged.pdf?sequence=-1&isAllowed=y) a prágai műszaki egyetemről.

### URDF
Az IMU-hoz is csinálunk egy új linket és joint-ot az URDF-ben, de ebben az esetben nem lesz sem piros kocka, se más megjelenése, egyszerűen a robot alvázának origójához van fixen rögzítve.

```xml
  <!-- IMU -->
  <joint name="imu_joint" type="fixed">
    <origin xyz="0 0 0" rpy="0 0 0" />
    <parent link="base_link"/>
    <child link="imu_link" />
  </joint>

  <link name="imu_link">
  </link>
```

### Gazebo plugin
A Gazebo plugin használata pedig a következő:

```xml
  <!-- IMU -->
  <gazebo>
    <plugin name="imu_controller" filename="libhector_gazebo_ros_imu.so">
      <robotNamespace>/</robotNamespace>
      <updateRate>50.0</updateRate>
      <bodyName>imu_link</bodyName>
      <topicName>imu/data</topicName>
      <accelOffset>0.0 0.0 0.0</accelOffset>
      <accelDrift>0.005 0.005 0.005</accelDrift>
      <accelGaussianNoise>0.005 0.005 0.005</accelGaussianNoise>
      <rateOffset>0.0 0.0 0.0</rateOffset>
      <rateDrift>0.005 0.005 0.005 </rateDrift>
      <rateGaussianNoise>0.005 0.005 0.005 </rateGaussianNoise>
      <yawDrift>0.005</yawDrift>
      <yawGaussianNoise>0.005</yawGaussianNoise>
    </plugin>
  </gazebo>
```

A topic név és a frekvencia mellett megadható a szimulált szenzorok zaj modellje is, ahol a nagyfrekvenciás zajmodell mellett a hosszútávú drift is megadható.

Nézzük meg ezúttal is a szimulációt az IMU-val:
```console
roslaunch bme_gazebo_sensors spawn_robot.launch
```
![alt text][image5]

### RViz
Az IMU jelének megjelenítése egy csúnya nagy lila nyíl (ami egyébként a gyorsulásvektort mutatja), aminek a mérete nem is állítható. Ennek az az oka, hogy ez az egyik RViz plugin tutorial anyaga:  
http://docs.ros.org/en/noetic/api/rviz_plugin_tutorials/html/display_plugin_tutorial.html

Ennél egy kicsit szebb megjelenítő az RViz IMU Plugin, aminek ez a ROS wiki oldala: http://wiki.ros.org/rviz_imu_plugin.

A Linux csomagkezelőjével egyszerűen fel tudjátok tenni:
```console
sudo apt install ros-noetic-rviz-imu-plugin
```

Ez egy jobban értelmezhető tengely jelölőt tesz a robotra az IMU jele alapján.
![alt text][image6]

A működését bármikor gyorsan ellenőrizhetjük, ha a Gazeboban egy kicsit megforgatjátok a robotot.
![alt text][image7]

## GPS
A GPS szenzorunk szimulációjához szintén a Hector plugin-jét használjuk, ezúttal nem szükséges kiegészítenünk az URDF fájlunkat, elegendő hozzáadni a Gazebo plugin-t, ami referenciaként a robot alvázára hivatkozik.

```xml
  <gazebo>
    <plugin name="gps_controller" filename="libhector_gazebo_ros_gps.so">
      <robotNamespace>/</robotNamespace>
      <updateRate>40</updateRate>
      <bodyName>base_link</bodyName>
      <frameId>base_link</frameId>
      <topicName>navsat/fix</topicName>
      <velocityTopicName>navsat/vel</velocityTopicName>
      <referenceLatitude>47.479049</referenceLatitude>
      <referenceLongitude>19.057787</referenceLongitude>
      <referenceHeading>0</referenceHeading>
      <referenceAltitude>0</referenceAltitude>
      <drift>0.0001 0.0001 0.0001</drift>
    </plugin>
  </gazebo>
```

A paraméterekről részletes leírást a [ROS wiki](http://wiki.ros.org/hector_gazebo_plugins#GazeboRosGps)-n olvashattok. A referencia szélességi és hosszúsági fokot a BME D épületére állítottam be.

# GPS waypoint követés
Készítsünk egy saját node-ot, ami képes GPS koordináták alapján vezetni a szimulált robotunkat!
Azt már a korábbi fejezetekből tudjuk, hogy a robot mozgatásához Twist típusú üzenetet kell küldenünk a `cmd_vel` topicba, de nézzük meg milyen topicokra kell feliratkoznunk!

![alt text][image13]

A robotunk abszolút pozícióját a `navsat/fix` topicban találjuk, ez egy `NavSatFix` típusú üzenet a `sensor_msgs` csomagból, tehát az alap ROS telepítés része. Ezen belül látjuk a latitude és longitude változókat.

A cél GPS koordinátához képest tehát már meg tudjuk határozni a távolságunkat sőt az irányt, a két GPS koordináta közötti szög különbséget (**bearing**) is, azonban nem tudjuk még, hogy ehhez képest milyen irányban áll a robotunk (**heading** vagy **yaw**). Ehhez szükségünk van a robotunk abszolút orientációjára a `/odom` topicból, ami pedig egy `Odometry` típusú üzenet a `nav_msgs` csomagból, tehát szintén az alap ROS telepítés része!

A ROS a robot orientációját quaternionokban adja meg, mi azonban az egyszerűség kedvéért ezt Euler szögekre konvertáljuk.

## Python script
Készítsük el tehát a `gps_waypoint_follower.py` scriptet, ami ezen a 4 GPS koordinátán vezeti keresztül a robotot, majd megáll:
```python
# Example waypoints [latitude, longitude]
waypoints = [[47.47908802923231, 19.05774719012997],
             [47.47905809688768, 19.05774697410133],
             [47.47907097650916, 19.05779319890401],
             [47.47907258024465, 19.05782379884820]]
```

A `gps_waypoint_follower.py` tartalma:
```python
#!/usr/bin/env python3

import math
import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler

def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)

def get_gps_coordinates(msg):
    global latitude, longitude
    latitude = msg.latitude
    longitude = msg.longitude
    #print(msg.latitude, msg.longitude)

def haversine(lat1, lon1, lat2, lon2):
    # Calculate distance
    R = 6378.137 # Radius of earth in km
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c * 1000 # in meters

    # Calculate heading
    y = math.sin(dLon) * math.cos(dLon)
    x = math.cos(lat1 * math.pi / 180) * math.sin(lat2 * math.pi / 180) - math.sin(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.cos(dLon)
    bearing = -math.atan2(y,x)

    return d, bearing

latitude, longitude = 0, 0
roll, pitch, yaw = 0, 0, 0

rospy.init_node('gps_waypoint_follower')

sub_odom = rospy.Subscriber ('/odom', Odometry, get_rotation)
sub_gps = rospy.Subscriber ('/navsat/fix', NavSatFix, get_gps_coordinates)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(10)

rospy.loginfo("GPS waypoint follower node has started!")

# Example waypoints [latitude, longitude]
waypoints = [[47.47908802923231, 19.05774719012997],
             [47.47905809688768, 19.05774697410133],
             [47.47907097650916, 19.05779319890401],
             [47.47907258024465, 19.05782379884820]]

cmd_vel = Twist()
cmd_vel.linear.x = 0
cmd_vel.angular.z = 0

waypointIndex = 0
while not rospy.is_shutdown():
    distance, bearing = haversine(latitude, longitude, waypoints[waypointIndex][0], waypoints[waypointIndex][1])

    # calculate heading error from yaw and bearing
    headingError = bearing - yaw

    rospy.loginfo("Distance: %.3f m, heading error: %.3f rad." % (distance, headingError))
    #rospy.loginfo("Bearing: %.3f rad, yaw: %.3f rad, error: %.3f rad" % (bearing, yaw, headingError))

    # Heading error, threshold is 0.1 rad
    if abs(headingError) > 0.1:
        # Only rotate in place if there is any heading error
        cmd_vel.linear.x = 0

        if headingError < 0:
            cmd_vel.angular.z = -0.3
        else:
            cmd_vel.angular.z = 0.3
    else:
        # Only straight driving, no curves
        cmd_vel.angular.z = 0
        # Distance error, threshold is 0.2m
        if distance > 0.2:
            cmd_vel.linear.x = 0.5
        else:
            cmd_vel.linear.x = 0
            rospy.loginfo("Target waypoint reached!")
            waypointIndex += 1

    pub.publish(cmd_vel)

    if waypointIndex == len(waypoints):
        rospy.loginfo("Last target waypoint reached!")
        break
    else:
        rate.sleep()
```

## Haversine formula
Mivel a GPS koordináták nem egy sík felület X, Y koordináta párjai, ezért szükségünk van egy speciális formulára, ami a szélességi és hosszúsági fokok alapján meghatározza a távolságot és az irányt a gömb felszínén. Erre a fenti kódban a [Haversine formulát](https://en.wikipedia.org/wiki/Haversine_formula) használjuk.

A képletben én a Föld sugarának az egyenlítői maximum 6378.137km-t használtam, de használhatnánk a pólusok minimum 6356.7523km-ét, vagy az átlag 6371.0088km-t.

Le is tesztelhetjük a Haversine képlet számításunkat egy egyszerű kis példaprogrammal:
```python
#!/usr/bin/env python3

import math

def haversine(lat1, lon1, lat2, lon2):
    # Calculate distance
    R = 6378.137 # Radius of earth in km
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c * 1000 # in meters

    # Calculate heading
    y = math.sin(dLon) * math.cos(dLon)
    x = math.cos(lat1 * math.pi / 180) * math.sin(lat2 * math.pi / 180) - math.sin(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.cos(dLon)
    bearing = -math.atan2(y,x)

    return d, bearing

# (lat, lon)
lyon = (45.7597, 4.8422) 
paris = (48.8567, 2.3508)
new_york = (40.7033962, -74.2351462)
london = (51.509865, -0.118092)

print(haversine(lyon[0],lyon[1],paris[0],paris[1]))
print(haversine(lyon[0],lyon[1],new_york[0],new_york[1]))
```

Indítsuk el a szimulációt, majd egy másik terminálban futtassuk az új node-unkat:
```console
roslaunch bme_gazebo_sensors spawn_robot.launch
```

```console
rosrun bme_gazebo_sensors gps_waypoint_follower.py
```

![alt text][image14]

## Helyes fordulás
A robot szépen odavezet az első koordinátához, azonban a második koordinátát nem képes elérni, csak egyhelyben forgolódik. Ennek az az oka, hogy a második koordináta hosszúsági foka közel azonos az első koordinátáéval, és emiatt a robotnak egyenesen "balra" kéne vezetnie. Az Euler szögekre való konvertálásnak viszont az a hátránya, hogy a szögtartományt [-pi, pi] radiánra konvertálja, aminek szakadása van 180 foknál. Erre az egyik megoldás a forgatás implementálása quaternionokban, ez azonban túlmutat ennek a tárgynak a keretein, így oldjuk meg ezt a szakadást a következő kódkiegészítéssel továbbra is Euler szögek használatával.

```python
    # calculate heading error from yaw and bearing
    headingError = bearing - yaw
    if headingError > math.pi:
        headingError = headingError - (2 * math.pi) 
    if headingError < -math.pi:
        headingError = headingError + (2 * math.pi)
```

Indítsuk újra a szimulációt!

![alt text][image15]

A robot így már képes végig vezetni az összes waypoint koordinátáján!

## Odometria vagy IMU használata

Mi a probléma a szimulációnkkal? A valóságban nincs ilyen pontos odometriánk, sőt az abszolút orientáció sem ismert induláskor!
Ezért használunk IMU-t, egy 6 tengelyes IMU-val (gyorsulásmérő + giroszkóp) már képesek vagyunk a gyorsulásmérő segítségével megtalálni a forgás tengelyét, a giroszkóp szögsebességeinek integrálásával pedig a pontos szöget. Ez a valóságban természetesen csak részben igaz, ugyanis a giroszkóp driftje miatt nagyon nehéz abszolút yaw mérésére használni. Az odometriával történő szenzorfúzióval ezt már egészen jól tudjuk kompenzálni, azonban ezzel csak egy későbbi leckében foglalkozunk.

Most elégedjünk meg az egyszerűbb megoldással, ha olyan IMU-t használunk, amiben van magnetométer, akkor a kalibráció után a gyorsulásmérőből származó adatokkal tudunk csinálni egy döntéskompenzált iránytűt, ami abszolút orientációt ad. A mostani szimulációnkban épp ilyen a szimulált IMU. Iratkozzunk hát fel erre a `/odom` topic helyett. Nézzük meg melyik topicra van szükségünk az rqt segítségével:

![alt text][image16]

Az `/imu/data` topic egy `Imu` típusú üzenet a `sensor_msgs` csomagból, ami a ROS konvencióinak köszönhetően ugyanúgy quaternionban adja vissza az orientációt, tehát azon kívül, hogy milyen topicra iratkozunk fel semmi mást sem kell módosítanunk a kódunkon!

```python
def get_imu_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
```

valamint

```python
#sub_odom = rospy.Subscriber ('/odom', Odometry, get_rotation)
sub_imu = rospy.Subscriber ('/imu/data', Imu, get_imu_rotation)
```

Próbáljuk ki újra a szimulációt!

![alt text][image17]

Nem tapasztalunk változást, ami ebben az esetben jó hír, a robot gond nélkül végigvezetett minden waypointon. Ennek a megoldásnak az az előnye, hogy sokkal közelebb áll egy valódi roboton futtatható megoldáshoz, mint az, ami túlzottan a szimuláció ideális pontosságára épít.

# Szenzorok 2
## Lidar

A lidarok olyan lézer scannerek, amik meghatározzák a szenzort körülvevő környezet egyes pontjainak távolságát. Ezeket a távolságokat egy pontfelhőben tárolják. Érdemes megkülönböztetni az egy síkban scannelő 2D lidarokat a 3D-s pontfelhőt generáló lidaroktól, ugyanis a 2D és 3D pontfelhőket máshogy tároljuk és máshogy is dolgozzuk fel. Csináljuk meg először egy 2D lidar szimulációját.

### URDF
Adjuk hozzá a `scan_link`-et és a hozzátatozó jointot az URDF fájlunkhoz.
```xml
  <!-- Lidar -->
  <joint type="fixed" name="scan_joint">
    <origin xyz="0.0 0 0.15" rpy="0 0 0"/>
    <child link="scan_link"/>
    <parent link="base_link"/>
    <axis xyz="0 1 0" rpy="0 0 0"/>
  </joint>

  <link name='scan_link'>
    <inertial>
      <mass value="1e-5"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia
          ixx="1e-6" ixy="0" ixz="0"
          iyy="1e-6" iyz="0"
          izz="1e-6"
      />
    </inertial>

    <collision name='collision'>
      <origin xyz="0 0 0" rpy="0 0 0"/> 
      <geometry>
        <box size=".1 .1 .1"/>
      </geometry>
    </collision>

    <visual name='scan_link_visual'>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <mesh filename = "package://bme_gazebo_sensors/meshes/lidar.dae"/>
      </geometry>
    </visual>

  </link>
```

Nézzük meg a lidar modelljét és elhelyezkedését a roboton:
```console
roslaunch bme_gazebo_sensors check_urdf.launch
```
![alt text][image18]

### Gazebo plugin
Adjuk hozzá a lidar pluginját a `mogi_bot.gazebo` fájlhoz:
```xml
  <!-- Lidar -->
  <gazebo reference="scan_link">
    <sensor type="ray" name="scan_sensor">
      <pose>0 0 0 0 0 0</pose>
      <visualize>false</visualize>
      <update_rate>40</update_rate>
      <ray>
        <scan>
          <horizontal>
            <samples>720</samples>
            <!--(max_angle-min_angle)/samples * resolution -->
            <resolution>1</resolution>
            <min_angle>-3.14156</min_angle>
            <max_angle>3.14156</max_angle>
          </horizontal>
        </scan>
        <range>
          <min>0.10</min>
          <max>10.0</max>
          <resolution>0.01</resolution>
        </range>
        <noise>
          <type>gaussian</type>
          <!-- Noise parameters based on published spec for Hokuyo laser
               achieving "+-30mm" accuracy at range < 10m.  A mean of 0.0m and
               stddev of 0.01m will put 99.7% of samples within 0.03m of the true
               reading. -->
          <mean>0.0</mean>
          <stddev>0.01</stddev>
        </noise>
      </ray>
      <plugin name="gazebo_ros_head_hokuyo_controller" filename="libgazebo_ros_laser.so">
        <topicName>/scan</topicName>
        <frameName>scan_link</frameName>
      </plugin>
    </sensor>
  </gazebo>
```
Lidarok esetén érdemes a paramétereket a szimulálni kívánt lidar alapján beállítani, például a szimulációban használt lidar [0 360] fok tartományon működik, és 720 mintát vesz ezen a tartományon, tehát a felbontása 0.5 fok.

Az első próbához kapcsoljuk be a szenzor működésének megjelenítését:
```xml
<visualize>true</visualize>
```
És indítsuk el a szimulációt:
![alt text][image19]

### RViz

Az RViz-ben látjuk, ahogy a lidar jelét megjeleníti a robot környezetében, mint 2D pontfelhőt, valamint azt is, hogy rávetíti az URDF-ben megadott transzformációknak megfelelően a kamera képére is!
![alt text][image20]

Ha megnöveljük a scan decay time-ját, akkor egy perzisztens pontfelhőt kapunk eredményül, ami gyakorlatilag a környezet térképének felel meg. Ez a szimulációnk ideális világában igaz is, azonban a térképezési algoritmusok ennél bonyolultabbak, a valóságban ez sajnos nem így működne. A térképezési algoritmusokat is megnézzük majd a következő leckében!
![alt text][image21]

## Velodyne VLP16 lidar

A szimulációnkban használhatunk 3D lidart is, ilyen például a Velodyne VLP16, ami teljes ROS és Gazebo szimuláció támogatással rendelkezik, amit elértek a DataspeedInc [bitbucket](https://bitbucket.org/DataspeedInc/velodyne_simulator/src/master/) repojában.

A plugin használatához telepítsük fel a `Velodyne Gazebo Plugins` csomagot, aminek ugyan van [ROS wiki](http://wiki.ros.org/velodyne_gazebo_plugins)-je, de valójában a dokumentáció a fenti [bitbucket](https://bitbucket.org/DataspeedInc/velodyne_simulator/src/master/) linken érhető el.
```console
sudo apt install ros-noetic-velodyne-gazebo-plugins
```

### URDF
A szimulációban cseréljük le a az előző `scan_link`-et az URDF fájlban.
```xml
  <!-- Velodyne -->
  <joint type="fixed" name="velodyne_joint">
    <origin xyz="0.0 0 0.10" rpy="0 0 0"/>
    <child link="velodyne_link"/>
    <parent link="base_link"/>
    <axis xyz="0 1 0" rpy="0 0 0"/>
  </joint>

  <link name='velodyne_link'>
    <inertial>
      <mass value="1e-5"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia
          ixx="1e-6" ixy="0" ixz="0"
          iyy="1e-6" iyz="0"
          izz="1e-6"
      />
    </inertial>

    <collision name='collision'>
      <origin xyz="0 0 0" rpy="0 0 0"/> 
      <geometry>
        <box size=".1 .1 .1"/>
      </geometry>
    </collision>

    <visual name='velodyne_link_visual'>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <mesh filename = "package://bme_gazebo_sensors/meshes/vlp16.dae"/>
      </geometry>
    </visual>

  </link>
```
És jelenítsük meg a robot modelljét az új Velodyne lidarral:
```console
roslaunch bme_gazebo_sensors check_urdf.launch
```
![alt text][image22]

### Gazebo plugin
Itt is cseréljük le az előző 2D lidar plugint, mivel helyette tesszük a robotra ezt a szenzort:
```xml
  <!-- Velodyne -->
  <gazebo reference="velodyne_link">
    <sensor type="ray" name="VLP16">
      <pose>0 0 0 0 0 0</pose>
      <visualize>false</visualize>
      <update_rate>10</update_rate>
      <ray>
        <scan>
          <horizontal>
            <samples>1875</samples>
            <resolution>1</resolution>
            <min_angle>-3.14156</min_angle>
            <max_angle>3.14156</max_angle>
          </horizontal>
          <vertical>
            <samples>16</samples>
            <resolution>1</resolution>
            <min_angle>-0.2618</min_angle>
            <max_angle>0.2618</max_angle>
          </vertical>
        </scan>
        <range>
          <min>0.3</min>
          <max>130.0</max>
          <resolution>0.001</resolution>
        </range>
        <noise>
          <type>gaussian</type>
          <mean>0.0</mean>
          <stddev>0.0</stddev>
        </noise>
      </ray>
      <plugin name="gazebo_ros_laser_controller" filename="libgazebo_ros_velodyne_laser.so">
        <topicName>velodyne_points</topicName>
        <frameName>velodyne_link</frameName>
        <min_range>0.9</min_range>
        <max_range>130.0</max_range>
        <gaussianNoise>0.008</gaussianNoise>
      </plugin>
    </sensor>
  </gazebo>
```
A Velodyne lidar paramétereit az eredeti VLP-16 alapján állítottam be, ami a hivatalos repoban [ezen a linken](https://bitbucket.org/DataspeedInc/velodyne_simulator/src/master/velodyne_description/urdf/VLP-16.urdf.xacro) található.

Indítsuk el a szimulációt, de előtte kapcsoljuk be a szenzor megjelenítését Gazeboban:
```xml
<visualize>false</visualize>
```

```console
roslaunch bme_gazebo_sensors spawn_robot.launch
```

![alt text][image23]

### RViz
RViz esetén a 3D lidar jeleit 3D pointcloud-ként jelenítjük meg, ahol például a Z tengely menti szintvonalakat változó szín jelöli:
![alt text][image24]

Mivel a 3D lidar szimulációja elég erőforrás igényes, így a próba után távolítsuk is el, és tegyük vissza a 2D lidar szimulációját!

## RGBD kamera

Az utolsó szenzor, aminek a szimulációjával foglalkozunk a manapság egyre elterjedtebb RGBD kamera, ami a 3 csatornás színes kép mellett az adott képpont kamerától mért távolságát is megadja. Ilyen kamerák az XBox Kinect, Intel Realsense vagy a ZED kamerák.

Az RGBD kamerák az utóbbi időben jelentősen elterjedtek, aminek a fő oka az áruk drasztikus csökkenése és a minőség javulása. Például egy Intel Realsense D435i kamera akár 1280 × 720 pixel felbontással ad mélységi képet, RGB képet pedig 1920 x 1080 pixel felbontással 30 FPS mellett. Továbbá rendelkezik beépített IMU-val és egy olyan lézer pötty projektorral, ami segít a távolságmérésben rossz fényviszonyok vagy textúra esetén.

Mivel a kameránknak már elkészítettük a linkjét, így az URDF fájlunkban nincs is szükség módosításra, csak a Gazebo plugint kell hozzáadnunk, ami a `libgazebo_ros_openni_kinect` plugint fogja használni.

```xml
  <!-- RGBD camera -->
  <gazebo reference="camera_link">
    <sensor type="depth" name="camera2">
      <always_on>1</always_on>
      <update_rate>20.0</update_rate>
      <visualize>false</visualize>             
      <camera>
        <horizontal_fov>1.047</horizontal_fov>  
        <image>
          <width>640</width>
          <height>480</height>
          <format>B8G8R8</format>
        </image>
        <clip>
          <near>0.5</near>
          <far>10.0</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_openni_kinect.so">
        <baseline>0.2</baseline>
        <alwaysOn>true</alwaysOn>
        <updateRate>0.0</updateRate>
        <cameraName>depth_camera</cameraName>
        <frameName>camera_link_optical</frameName>                   
        <imageTopicName>rgb/image_raw</imageTopicName>
        <depthImageTopicName>depth/image_raw</depthImageTopicName>
        <pointCloudTopicName>depth/points</pointCloudTopicName>
        <cameraInfoTopicName>rgb/camera_info</cameraInfoTopicName>              
        <depthImageCameraInfoTopicName>depth/camera_info</depthImageCameraInfoTopicName>            
        <pointCloudCutoff>0.5</pointCloudCutoff>
        <pointCloudCutoffMax>10.0</pointCloudCutoffMax>
        <hackBaseline>0.0</hackBaseline>
        <distortionK1>0.0</distortionK1>
        <distortionK2>0.0</distortionK2>
        <distortionK3>0.0</distortionK3>
        <distortionT1>0.0</distortionT1>
        <distortionT2>0.0</distortionT2>
        <CxPrime>0.0</CxPrime>
        <Cx>0.0</Cx>
        <Cy>0.0</Cy>
        <focalLength>0.0</focalLength>
      </plugin>
    </sensor>
  </gazebo>
```

És indítsuk el a szimulációt!

```console
roslaunch bme_gazebo_sensors spawn_robot.launch
```

![alt text][image25]

Nézzük meg a kamerák képét rqt-ben is!

![alt text][image26]

A 3D pontfelhőn kívül egy szürkeárnyalatos mélységi képet is kapunk a távolságadatokról, ami minél világosabb annál távolabb van az adott pont. Minél magasabb a
```xml
<pointCloudCutoffMax>10.0</pointCloudCutoffMax>
```
paraméter értéke, annál messzebb lát el a kameránk, de annál erőforrásigényesebb is a szimulációja. Állítsuk most át ezt 3 méterre és nézzük meg a kamerák képeit rqt-ben!

![alt text][image27]

Vegyük észre, hogy ebben az esetben minden képpont, ami kívül esik a kamera érzékelési tartományán teljesen fekete.

# Képfeldolgozás ROS-ban OpenCV-vel
Ha képfeldolgozás, akkor nem is kérdés, hogy OpenCV-t fogunk használni. Természetesen léteznek más ingyenes és nyílt forrású képfeldolgozásra specializált library-k, Python esetén például a PIL/Pillow, a scikit-image, vagy megoldhatnánk mindent numpy-ból is, de szinte minden esetben biztosra megyünk, ha az OpenCV mellett döntünk. Főleg mert a ROS-hoz hasonlóan nagyon széleskörűen használt és jól dokumentált C++ és Python API-val rendelkezik, ami sokkal egyszerűbb átjárást biztosít a nyelvek között, mint egy olyan megoldás, ami csak Python esetén érhető el.

A ROS egy alap csomagjának segítségével, a [cv_bridge](http://wiki.ros.org/cv_bridge) segítségével könnyű átjárást biztosít a ROS és az OpenCV között. Könnyedén tudunk ROS üzenetből OpenCV image-et készíteni és az OpenCV image is könnyedén ROS üzenetté konvertálható.

Én a kód elkészítése során OpenCV 4.6.0 verziót használtam, amit egyszerűen a Python csomagkezelőjével, a pip-pel tudtok telepíteni.
Mivel a pip automatikusan a legfrissebb változatot fogja telepíteni, ami az adott Python verzióhoz elérhető, így, ha egy konkrét verziót szeretnétek feltenni, használjátok a `pip install opencv-python==$VERSION` parancsot, ahol a $VERSION természetesen az a verzió, amit szeretnétek kiválasztani. Hogy milyen verziók érhetők el, az könnyen kilistázható a pip-pel:

```console
david@david-precision-7520:~/bme_catkin_ws/src/Week-5-6-Gazebo-sensors/bme_gazebo_sensors/scripts$ pip install opencv-python==
ERROR: Could not find a version that satisfies the requirement opencv-python== (from versions: 3.4.0.14, 3.4.8.29, 3.4.9.31, 3.4.9.33, 3.4.10.35, 3.4.10.37, 3.4.11.39, 3.4.11.41, 3.4.11.43, 3.4.11.45, 3.4.13.47, 3.4.14.51, 3.4.14.53, 3.4.15.55, 3.4.16.57, 3.4.16.59, 3.4.17.61, 3.4.17.63, 3.4.18.65, 4.1.2.30, 4.2.0.32, 4.2.0.34, 4.3.0.36, 4.3.0.38, 4.4.0.40, 4.4.0.42, 4.4.0.44, 4.4.0.46, 4.5.1.48, 4.5.2.52, 4.5.2.54, 4.5.3.56, 4.5.4.58, 4.5.4.60, 4.5.5.62, 4.5.5.64, 4.6.0.66)
ERROR: No matching distribution found for opencv-python==

```

## ROS node

Ezúttal is egy Python node-ot fogunk készíteni az egyszerűség kedvéért. Az OpenCV és Numpy library-knak telepítve kell lenniük a Pythonotokhoz a kód használatához. Hozzuk létre a `chase_the_ball.py` fájlt a scripts mappában.

```python
#!/usr/bin/env python3

import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CompressedImage
from geometry_msgs.msg import Twist
import rospy
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
import threading
import numpy as np

class BufferQueue(Queue):
    """Slight modification of the standard Queue that discards the oldest item
    when adding an item and the queue is full.
    """
    def put(self, item, *args, **kwargs):
        # The base implementation, for reference:
        # https://github.com/python/cpython/blob/2.7/Lib/Queue.py#L107
        # https://github.com/python/cpython/blob/3.8/Lib/queue.py#L121
        with self.mutex:
            if self.maxsize > 0 and self._qsize() == self.maxsize:
                self._get()
            self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()

class cvThread(threading.Thread):
    """
    Thread that displays and processes the current image
    It is its own thread so that all display can be done
    in one thread to overcome imshow limitations and
    https://github.com/ros-perception/image_pipeline/issues/85
    """
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.image = None

        # Initialize published Twist message
        self.cmd_vel = Twist()
        self.cmd_vel.linear.x = 0
        self.cmd_vel.angular.z = 0

    def run(self):
        # Create a single OpenCV window
        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("frame", 800,600)

        while True:
            self.image = self.queue.get()

            # Process the current image
            mask, contour, crosshair = self.processImage(self.image)

            # Add processed images as small images on top of main image
            result = self.addSmallPictures(self.image, [mask, contour, crosshair])
            cv2.imshow("frame", result)

            # Check for 'q' key to exit
            k = cv2.waitKey(6) & 0xFF
            if k in [27, ord('q')]:
                rospy.signal_shutdown('Quit')

    def processImage(self, img):

        rows,cols = img.shape[:2]

        R,G,B = self.convert2rgb(img)

        redMask = self.thresholdBinary(R, (220, 255))
        stackedMask = np.dstack((redMask, redMask, redMask))
        contourMask = stackedMask.copy()
        crosshairMask = stackedMask.copy()

        # return value of findContours depends on OpenCV version
        (contours,hierarchy) = cv2.findContours(redMask.copy(), 1, cv2.CHAIN_APPROX_NONE)

        # Find the biggest contour (if detected)
        if len(contours) > 0:
            
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            # Make sure that "m00" won't cause ZeroDivisionError: float division by zero
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0

            # Show contour and centroid
            cv2.drawContours(contourMask, contours, -1, (0,255,0), 10)
            cv2.circle(contourMask, (cx, cy), 5, (0, 255, 0), -1)

            # Show crosshair and difference from middle point
            cv2.line(crosshairMask,(cx,0),(cx,rows),(0,0,255),10)
            cv2.line(crosshairMask,(0,cy),(cols,cy),(0,0,255),10)
            cv2.line(crosshairMask,(int(cols/2),0),(int(cols/2),rows),(255,0,0),10)

            # Chase the ball
            #print(abs(cols - cx), cx, cols)
            if abs(cols/2 - cx) > 20:
                self.cmd_vel.linear.x = 0
                if cols/2 > cx:
                    self.cmd_vel.angular.z = 0.2
                else:
                    self.cmd_vel.angular.z = -0.2

            else:
                self.cmd_vel.linear.x = 0.2
                self.cmd_vel.angular.z = 0

        else:
            self.cmd_vel.linear.x = 0
            self.cmd_vel.angular.z = 0

        # Publish cmd_vel
        pub.publish(self.cmd_vel)

        # Return processed frames
        return redMask, contourMask, crosshairMask

    # Convert to RGB channels
    def convert2rgb(self, img):
        R = img[:, :, 2]
        G = img[:, :, 1]
        B = img[:, :, 0]

        return R, G, B

    # Apply threshold and result a binary image
    def thresholdBinary(self, img, thresh=(200, 255)):
        binary = np.zeros_like(img)
        binary[(img >= thresh[0]) & (img <= thresh[1])] = 1

        return binary*255

    # Add small images to the top row of the main image
    def addSmallPictures(self, img, small_images, size=(160, 120)):
        '''
        :param img: main image
        :param small_images: array of small images
        :param size: size of small images
        :return: overlayed image
        '''

        x_base_offset = 40
        y_base_offset = 10

        x_offset = x_base_offset
        y_offset = y_base_offset

        for small in small_images:
            small = cv2.resize(small, size)
            if len(small.shape) == 2:
                small = np.dstack((small, small, small))

            img[y_offset: y_offset + size[1], x_offset: x_offset + size[0]] = small

            x_offset += size[0] + x_base_offset

        return img

def queueMonocular(msg):
    try:
        # Convert your ROS Image message to OpenCV2
        cv2Img = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
    except CvBridgeError as e:
        print(e)
    else:
        qMono.put(cv2Img)

print("OpenCV version: %s" % cv2.__version__)

queueSize = 1      
qMono = BufferQueue(queueSize)

cvThreadHandle = cvThread(qMono)
cvThreadHandle.setDaemon(True)
cvThreadHandle.start()

bridge = CvBridge()

rospy.init_node('ball_chaser')
# Define your image topic
image_topic = "/head_camera/image_raw"
# Set up your subscriber and define its callback
rospy.Subscriber(image_topic, Image, queueMonocular)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
# Spin until Ctrl+C
rospy.spin()
```

> **_Például OpenCV 3.x.x esetén a `cv2.findContours` még 3 visszatérési értékkel rendelkezett, így ott le kellett cserélnünk a következő sort:_** 
> ```python
> # return value of findContours depends on OpenCV version
> (_,contours,hierarchy) = cv2.findContours(redMask.copy(), 1, cv2.CHAIN_APPROX_NONE)
> ```

Nézzük a kódot! Importáljuk be a szükséges library-kat, ilyen az OpenCV (`cv2`) a `numpy` és a `cv_bridge`, valamint a szükséges ROS üzenettípusok.
Egy speciális queue-t fogunk használni a kódban a képkockák tárolására és a `threading` segítségével egy több szálon futó kódot készítünk.

```python
#!/usr/bin/env python3

import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image, CompressedImage
from geometry_msgs.msg import Twist
import rospy
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
import threading
import numpy as np
```

A queue-nk annyiban különleges, hogy abban az esetben, ha már tele van, nem dobja el a következő be már nem férő képkockát, hanem helyette üríti belőle a korábbit.

```python
class BufferQueue(Queue):
    """Slight modification of the standard Queue that discards the oldest item
    when adding an item and the queue is full.
    """
    def put(self, item, *args, **kwargs):
        # The base implementation, for reference:
        # https://github.com/python/cpython/blob/2.7/Lib/Queue.py#L107
        # https://github.com/python/cpython/blob/3.8/Lib/queue.py#L121
        with self.mutex:
            if self.maxsize > 0 and self._qsize() == self.maxsize:
                self._get()
            self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()
```

A `cvThread`-ben történik a képek feldolgozása és megjelenítése, és ezen kívül 3 helper function is található benne, amik segítenek a képkockák feldolgozásában. Vegyük észre, hogy az OpenCV képkockáinkban a csatornák sorrendje BGR és nem RGB!
```python
    # Convert to RGB channels
    def convert2rgb(self, img):
        R = img[:, :, 2]
        G = img[:, :, 1]
        B = img[:, :, 0]

        return R, G, B

    # Apply threshold and result a binary image
    def thresholdBinary(self, img, thresh=(200, 255)):
        binary = np.zeros_like(img)
        binary[(img >= thresh[0]) & (img <= thresh[1])] = 1

        return binary*255

    # Add small images to the top row of the main image
    def addSmallPictures(self, img, small_images, size=(160, 120)):
        '''
        :param img: main image
        :param small_images: array of small images
        :param size: size of small images
        :return: overlayed image
        '''

        x_base_offset = 40
        y_base_offset = 10

        x_offset = x_base_offset
        y_offset = y_base_offset

        for small in small_images:
            small = cv2.resize(small, size)
            if len(small.shape) == 2:
                small = np.dstack((small, small, small))

            img[y_offset: y_offset + size[1], x_offset: x_offset + size[0]] = small

            x_offset += size[0] + x_base_offset

        return img
```

A kód további része pedig egyszerűen létrehozza a queue-t és a threadet, feliratkozik a `/head_camera/image_raw` topicra, valamint létrehoz egy `/cmd_vel` publishert. A `/head_camera/image_raw` topicra való feliratkozás callback függvénye a `queueMonocular`, ami a `cv_bridge` segítségével már OpenCV kompatibilis képkockákat tesz a queue-nkba.

```python
def queueMonocular(msg):
    try:
        # Convert your ROS Image message to OpenCV2
        cv2Img = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
    except CvBridgeError as e:
        print(e)
    else:
        qMono.put(cv2Img)

print("OpenCV version: %s" % cv2.__version__)

queueSize = 1      
qMono = BufferQueue(queueSize)

cvThreadHandle = cvThread(qMono)
cvThreadHandle.setDaemon(True)
cvThreadHandle.start()

bridge = CvBridge()

rospy.init_node('ball_chaser')
# Define your image topic
image_topic = "/head_camera/image_raw"
# Set up your subscriber and define its callback
rospy.Subscriber(image_topic, Image, queueMonocular)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
# Spin until Ctrl+C
rospy.spin()
```

Ne feledkezzünk el a fájl futtatható tételéről a `chmod +x` paranccsal, és indítsuk el a szimulációt, valamint az új node-unkat!
```console
roslaunch bme_gazebo_sensors spawn_robot.launch
```

valamint:
```console
rosrun bme_gazebo_sensors chase_the_ball.py
```

Indulás után ezt látjuk:  
![alt text][image31]

Szükségünk van valami piros objektumra, amit követhetünk, hiszen így állítottuk be a szűrési paraméterünket a `processImage` függvényünkben!
```python
R,G,B = self.convert2rgb(img)

redMask = self.thresholdBinary(R, (220, 255))
```

## Adjunk hozzá egy piros labdát

Ha még nincs piros labdánk a meglévő modelljeink között, csináljunk egyet a model editorral:
![alt text][image28]

Mentsük el és utána már bármikor elérhető lesz az insert fül alatt.
![alt text][image29]

Láthatjuk, hogy a node-unk színszűrése most már észre is veszi a labdát, megkeresi a kontúrját, valamint a kontúr centroidját, és a centroid alapján mozgatja a robotot, amíg a labda épp a kamerával szembe nem kerül.

![alt text][image30]

És végül a videó a működésről, amit a bevezetés során már láttunk:

<a href="https://youtu.be/-YCcQZmKJtY"><img height="400" src="./assets/youtube2.png"></a>