# Multi-View-V-SLAM
The main idea problem statement of this project is to provide an affordable solution to map 3D environments(preferably indoor)

It is generally expensive to have high resolution cameras (or even LiDARs) for indoor robots which are expected to be affordable. We instead make use of multiple low-res cameras mounted using any kind of motors. We also have a central camera fixed with respect ti the chassis of the robot. These rotating cameras keep tracking a particular feature point throughout the duration of it's visibility. 
This gives us a few advantages: 
  -> The feature point is being tracked for more time than usual, so we can get more number of readings and therefore better accuracy.
  -> As we keep focussing the feature point at the center of the respective camera, we needn't worry about extrapolating it's location using classic computer based methods (Which require good resolution and parameters of the cameras), instead we use the angle provided by the motor itself.

As you can see, we no longer need a high resolution, high FOV camera.

Using these few points that are more accurately mapped, we form an optimization function for the rest of the map with these points as the anchors.

The full presentation of the project can be found in "MView_VSLAM.pdf" .
The python code can be found in the branch "code". This being a course project, we failed to push the complete working code after
  the course grading is done. 
