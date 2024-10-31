#app/src/main/python/yolov3.weights
 - Run the project and grant the necessary permissions.
## call services from adb ##
adb shell am start-foreground-service -a com.example.DetectionService 
## stop services from adb ##
adb shell am startservice -a com.example.StopService
## use logcat to see the results
adb logcat -d | grep "Result Detect:"

