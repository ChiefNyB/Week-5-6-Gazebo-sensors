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

# 5. - 6. hét - Szenzorok szimulációja Gazeboban

# Hova fogunk eljutni?

<a href="https://youtu.be/xxx"><img height="400" src="./assets/youtube.png"></a>

# Tartalomjegyzék
1. [Kezdőcsomag](#Kezdőcsomag)
2. [A `tree` parancs](#A-`tree`-parancs)
3. [Szenzorok 1](#Szenzorok-1)
4. [Waypoint követés](#Waypoint-követés)
5. [Szenzorok 2](#Szenzorok-2)
6. [OpenCV](#OpenCV)

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
A mappák tartalma egyszerűen listázható így a `tree` paranccsal, ha csak bizonyos mélységig szeretnétek listázni, akkor megtehetitek a `-L` kapcsoló segítségével. Példul `tree -L 2`.

# Szenzorok 1
## Kamera
A kamera hozzáadása két lépésben történik, először adjuk hozzá a kamerát a robotunk URDF fájljához.
A kamera egy új link lesz `camera_link` néven, ami fixed jointtal csatlakozik a robot alvázához. Az egyszerűség kedvéért, legyen a kameránk egy kis piros kocka.

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

A kamerákat használhatunk ROS esetén a transzformációk megadása nélkül is, azonban ez a gyakorlatban nem praktikus, mert az RViz képes a megjelenített adatokat a transzformációknak megfelelően overlay-elni a kamera képére. Ez csak akkor működik, ha a kameránk transzformációját megadtuk (és helyesen adtuk meg) az URDF fájlban.

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

A kamera képére ráközelítve láthatjátok az overlayt. Ez a későbbiekben, ahol több szenzort is adunk majd a robotunkhoz hasznosabb és látványosabb lesz.

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

Az RViz után nézzük meg a kamera által küldött topicokat rqt-ben is:
![alt text][image10]

A szimulált kamera alapértelmezetten a `/head_camera/image_raw` topicban küldi a kamera streamet. Ezt a plugin beállításainál a következő paraméterekkel adtuk meg:
```xml
<cameraName>head_camera</cameraName>
<imageTopicName>image_raw</imageTopicName>
```

### Videótömörítés

ROS esetén a kamera alapértelmezetten az [image transport](http://wiki.ros.org/image_transport) csomag segjtségével küldi a tömörítetlen streamet. Ez ennek megfelelően nagy sávszélességet is igényel. Ez egy mobil robot esetén ahol 1 vagy több kamera képét egy másik hálózati gépen is szeretnénk elérni nem elfogadható terhelés a hálózaton.

A megoldás a kamera stream tömörítése, ROS esetén szerencsére ehhez sem kell saját alkalmazást fejleszteni, ugyanis az image transport csomag kezel plugineket. ROS esetén a két legelterjedtebb plugin a [compressed image transport](http://wiki.ros.org/compressed_image_transport) valamint a [theora image transport](http://wiki.ros.org/theora_image_transport).

Ezeket a csomagokat csak egyszerűen telepítenünk kell és automatikusan megjelennek a tömörített képet tartalmazó topicok.
A compressed image transport konfigurálható jpg vagy png tömörítéssel, valamint a tömörítés mértékével.

De még ennél is szignifikánsan kisebb streamet eredményez a [theora tömörítés](https://en.wikipedia.org/wiki/Theora), ami egy teljesen nyílt forrású és ingyenes videótömörítési eljárás.

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

ToDo: mi a az IMU

IMU szimulációra több Gazebo plugin is létezik, én az alábbi Hector IMU controllert használom itt, ami a [Darmstadt-i egyetem](https://www.teamhector.de/) fejlesztése, és itt találjátok a ROS Wiki-n: http://wiki.ros.org/hector_gazebo_plugins.

A Linux csomagkezelőjével egyszerűen fel tudjátok tenni:
```console
sudo apt install ros-melodic-hector-gazebo-plugins
```

Az IMU-hoz is csinálunk egy új linket és jointot, de ebben az esetben nem lesz semmi megjelenése, egyszerűen a robot alvázának origójához van fixen rögzítve.

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

A Gazebo plugin pedig a következő:

```xml
  <!-- IMU -->
  <gazebo>
    <plugin name="imu_controller" filename="libhector_gazebo_ros_imu.so">
      <robotNamespace>/</robotNamespace>
      <updateRate>50.0</updateRate>
      <bodyName>imu_link</bodyName>
      <topicName>imu/data</topicName>
      <accelDrift>0.005 0.005 0.005</accelDrift>
      <accelGaussianNoise>0.005 0.005 0.005</accelGaussianNoise>
      <rateDrift>0.005 0.005 0.005 </rateDrift>
      <rateGaussianNoise>0.005 0.005 0.005 </rateGaussianNoise>
      <headingDrift>0.005</headingDrift>
      <headingGaussianNoise>0.005</headingGaussianNoise>
    </plugin>
  </gazebo>
```

ToDo: paraméterek.

Nézzük meg ezúttal is a szimulációt az IMU-val:
```console
roslaunch bme_gazebo_sensors spawn_robot.launch
```
![alt text][image5]

Az IMU jelének megjelenítése egy csúnya nagy lila nyíl, aminek a scale-je nem is állítható. Ennek az az oka, hogy ez az egyik RViz plugin tutorial anyaga:  
http://docs.ros.org/en/melodic/api/rviz_plugin_tutorials/html/display_plugin_tutorial.html

Ennél egy kicsit szebb megjelenítő az RViz IMU Plugin, aminek ez a ROS wiki oldala: http://wiki.ros.org/rviz_imu_plugin.

A Linux csomagkezelőjével egyszerűen fel tudjátok tenni:
```console
sudo apt install ros-melodic-rviz-imu-plugin
```

Ez egy jobban értelmezhető tengely jelölőt tesz a robotra az IMU jele alapján.
![alt text][image6]

A működését bármikor gyorsan ellenőrízhetitek, ha a Gazeboban egy kicsit megforgatjátok a robotot.
![alt text][image7]

## GPS


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


# Waypoint követés
https://en.wikipedia.org/wiki/Haversine_formula

Odometria vs IMU


# Szenzorok 2
## Lidar


## Velodyne VLP16 lidar
https://bitbucket.org/DataspeedInc/velodyne_simulator/src/master/

Paramterek:
https://bitbucket.org/DataspeedInc/velodyne_simulator/src/master/velodyne_description/urdf/VLP-16.urdf.xacro

## RGBD kamera

# cv bridge és OpenCV