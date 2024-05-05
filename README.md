Bu kod, bir yemek tarifi uygulaması oluşturur ve kullanıcılara tarif eklemelerini, 
aramalarını ve değerlendirmelerini sağlar. İşlevselliği şu şekilde özetlenebilir:

Tarif Uygulamasi Sınıfı: Ana uygulama penceresini oluşturur ve temel arayüz öğelerini içerir. 
Kullanıcılar, tarif adı, malzemeler ve tarif metni girerek yeni tarifler ekleyebilirler. 
Ayrıca, mevcut tarifleri arayabilir ve değerlendirme penceresini açabilirler.

Tarif Arama Sınıfı: Tarif arama penceresini oluşturur. 
Kullanıcılar, arama metni girerek tarifleri arayabilir ve bulunan sonuçları görüntüleyebilirler. 
Ayrıca, tarifin değerlendirme puanını da görüntüler.

Tarif Degerlendir Sınıfı: Tarifi değerlendirme penceresini oluşturur. 
Kullanıcılar, seçtikleri tarifi bir metin ve bir puanla değerlendirebilirler. 
Değerlendirme sonrasında, puan verilen tarifin puanı güncellenir.
Uygulama ayrıca, SQLite veritabanı kullanarak tarifleri saklar ve uygulama her başladığında bu veritabanına bağlanır. 
PyQt5 widget'larını kullanarak arayüz öğeleri oluşturur ve özel stiller ve temalar uygular.

Bu şekilde, kullanıcılar yemek tariflerini ekleyebilir, arayabilir ve değerlendirebilirler.
