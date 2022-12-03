## <p><img width="50" src="https://www.icloud.com.cn/system/icloud.com/2302Hotfix226/en-us/32f2db22e40a7765c151f4d947c2be50.png"> <text backgournd-color="red">获取设备地理位置(查找我的iPhone)</text></p> 

[//]: # (![]&#40;https://www.icloud.com.cn/system/icloud.com/2302Hotfix226/en-us/32f2db22e40a7765c151f4d947c2be50.png&#41;)
```python
api.iphone.location()
```

```json
{
  'isOld': True,
  'isInaccurate': False,
  'positionType': 'Wifi',
  'secureLocation': None,
  'secureLocationTs': 0,
  'altitude': 0.0,
  'latitude': 43.894873066105184,//纬度
  'longitude': 87.58595865485619,//经度
  'horizontalAccuracy': 65.0,//水平精度
  'verticalAccuracy': 0.0,//垂直精度
  'timeStamp': 1670048465162,//时间戳
  'floorLevel': 0,
  'locationType': '',
  'locationFinished': True,
  'locationMode': None
}
```
