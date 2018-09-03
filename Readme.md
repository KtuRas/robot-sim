# Otonom Robot Simülasyonu

Bu Repo' da turtlebot3 simulasyon modeli kullanılarak derin öğrenme testleri yapılmıştır. 

Derin öğrenme framework' u olarak tensorflow alt yapısında çalışan keras kullanılmıştır. Eğitimler test pistinde araç önce ileri doğru sonra geri doğru giderken verilerin kaydedilmesi ile yapılmıştır.

Bu ros paketinin çalışması için aşağıdaki paketlere ihtiyaç vardır.
* tensorflow / theano
* keras
* turtlebot3
* turtlebot3-simulations

Yapay sinir ağında eğitilmek üzere simülasyon ortamındaki robottan lidar verisini ve kamera verisini alınır. Ancak bu veri doğrudan doğrudan sinir ağına gönderilmez. Lidar verisi olarak robotun ön tarafındaki 120 derecelik açı içerisindeki veriler kullanılır. Kameradan gelen görüntüden bir ROI belirlenir. Bu ROI robotun sadece ön tarafını görecek şekilde seçilir. Böylece robotun arka tarafındaki objeler ile gökyüzü ve duvarların üst tarafları sinir ağında karmaşaya yol açmazlar. 

"scripts" klasörünün içerisinde kaynak kodlar bulunmakta. Python dili ilie oluşturulmuş yazılım dosyalarının işlevleri aşağıdaki gibidir.
* my_joy.py : ros ile çalışan joystick verileri cmd_vel' e çeviren yazılım 
* get_data.py : rosbag dosyasındaki verileri numpy formatına çevirip kaydeden yazılım
* my_train.py : daha önceden numpy veri tipinde kaydedilmiş verileri keras ile oluşturan yapay sinir ağında öğreten yazılım
* my_predict.py : keras ile oluşturulmuş ağırlık (weights) dosyalarını kullanarak gerçek zamanlı tahmin yapan yazılım 

Simülasyonu başlatmak için

* roslaunch robot_sim start_sim.launch

Simülasyonu eğitim yada tahmin modunda başlatmak için 

* robot-sim/launch/start_sim.launch

dosyasındaki "mode" parametresini test olarak değiştirin.

Benzer duvar ve yer desenli farklı bir pistte eğitilen aracın pistte otonom olarak sürüşüne [bağlantıdan](https://www.youtube.com/watch?v=FVX2JWJV_X4&t=22s) ulaşabilirsiniz.

<img src="imgs/robot-gif.gif" width="1000px"/>