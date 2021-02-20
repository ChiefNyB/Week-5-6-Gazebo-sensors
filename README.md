[//]: # (Image References)

[image1]: ./assets/mogi_bot_camera_1.png "Camera"
[image2]: ./assets/mogi_bot_camera_2.png "Camera"
[image3]: ./assets/mogi_bot_camera_3.png "Camera"
[image4]: ./assets/mogi_bot_camera_4.png "Camera"
[image5]: ./assets/mogi_bot_lidar_1.png "Lidar"
[image6]: ./assets/mogi_bot_lidar_2.png "Lidar"
[image7]: ./assets/mogi_bot_lidar_3.png "Lidar"
[image8]: ./assets/mogi_bot_lidar_4.png "Lidar"
[image9]: ./assets/velodyne_1.png "Velodyne" 
[image10]: ./assets/velodyne_2.png "Velodyne" 


# 5. - 6. hét - Szenzorok szimulációja Gazeboban

# Hova fogunk eljutni?

<a href="https://youtu.be/xxx"><img height="400" src="./assets/youtube.png"></a>

# Kezdőcsomag
A lecke kezdőcsomagja épít a Week-3-4-Gazebo-basics anyagára, de egy külön GIT repositoryból dolgozunk, így nem feltétele az előző `bme_gazebo_basics` csomag megléte.

A kiindulási projekt tartalmazza a Gazebo világ szimulációját, az alap differenciálhajtású MOGI robotunk modelljét és szimulációját, valamint az alap launchfájlokat és RViz fájlokat.

# Kamera
A kamera hozzáadása két lépésben történik, először adjuk hozzá a kamerát a robotunk URDF fájljához.
A kamera egy új link lesz `camera_link` néven, ami fixed jointtal csatlakozik a robot alvázához. Az egyszerűség kedvéért, legyen a kameránk egy kis piros kocka.

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

A kameránkat használhatjuk ROS esetén a transzformáció megadása nélkül is, azonban ez a gyakorlatban nem praktikus, mert az RViz képes a megjelenített adatokat a transzformációnak megfelelően overlay-elni a kamera képére. Ez csak akkor működik, ha a kameránk transzformációját helyesen adjuk meg az URDF fájlban.

A Gazebo és az RViz kamera transzformációja között azonban van némi ellentmondás, és ha csak a fenti sorok szerepelnek az URDF-ben helytelen lesz a kamera képére vetített overlay.

Ezt egy újabb link, a `camera_link_optical` segítségével tudjuk megoldani, ahol meg tudjuk oldani a további szükséges transzformációkat.
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

Ha elégedettek vagyunk a kamera helyzetével, hozzuk létre a Gazebo plugint, ami a kameránk szimulációját csinálja:
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

```console
roslaunch bme_gazebo_sensors spawn_robot.launch
```

# IMU
http://wiki.ros.org/hector_gazebo_plugins

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

# GPS

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


Waypoint követés
https://en.wikipedia.org/wiki/Haversine_formula


# Lidar


# Velodyne VLP16 lidar
https://bitbucket.org/DataspeedInc/velodyne_simulator/src/master/

Paramterek:
https://bitbucket.org/DataspeedInc/velodyne_simulator/src/master/velodyne_description/urdf/VLP-16.urdf.xacro

# RGBD kamera

# cv bridge OpenCV