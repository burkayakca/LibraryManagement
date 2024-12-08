
# Kütüphane Yönetim Sistemi

Bu dökümantasyon, Kütüphane Yönetim Sistemi için Python'da yazılmış bir uygulamayı açıklamaktadır. 
Uygulama, kitap ve üye bilgilerini JSON dosyaları kullanarak yönetir ve aşağıdaki işlevleri içerir:

## Özellikler

1. **Kitap Yönetimi**: Kitap ekleme, silme ve ödünç verme/iade işlemleri.
2. **Üye Yönetimi**: Yeni üye ekleme, silme ve üye bilgilerini görüntüleme.
3. **Veritabanı Yönetimi**: JSON dosyaları aracılığıyla kitap ve üye bilgilerini kaydetme.

## Kullanılan Sınıflar ve Metodlar

### `readDatabase()`
Veritabanını okur ve döner. Dosya eksikse `False` döner.

### `Book`
Kitap bilgilerini saklar:
- `name`: Kitap adı
- `author`: Yazar adı
- `year`: Yayın yılı
- `publisher`: Yayınevi

### `Member`
Üye bilgilerini saklar:
- `name`: Üye adı
- `phoneNumber`: Telefon numarası
- `email`: E-posta adresi
- `address`: İkamet adresi

### `Library`
Kütüphane yönetimi için ana sınıf. 

#### Metodlar:
- `addBook()`: Yeni kitap ekler.
- `removeBook(bookID)`: Kitap siler.
- `addMember()`: Yeni üye ekler.
- `deleteMember(MemberID)`: Üye siler.
- `lendBook(MemberID, bookID)`: Kitabı ödünç verir.
- `returnBook(MemberID, bookID)`: Kitabı iade alır.
- `validate(object, id)`: Kitap veya üye varlığını kontrol eder.

## Menü Seçenekleri

- **0**: Kitap Listesi
- **1**: Üye Listesi
- **2**: Kitap Ekle
- **3**: Kitap Sil
- **4**: Üye Ekle
- **5**: Üye Sil
- **6**: Kitap Ödünç Ver
- **7**: Kitap İade Al
- **8**: Çıkış

### Örnek Kullanım
```python
library = Library()
library.addBook()
library.lendBook(1, 1001)
library.returnBook(1, 1001)
```

