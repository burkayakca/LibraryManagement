import random

class Book:
    def __init__(self,name,author,year,publisher):
        self.name = name
        self.author = author
        self.year = year
        self.publisher = publisher

class Member:
    def __init__(self,name,phoneNumber,email,address):
        self.name = name
        self.phoneNumber = phoneNumber
        self.email = email
        self.address = address

class Library:
    def __init__(self):
        self.collection = { 64 : {
            "name" : "Moby Dick",
            "author" : "Herman Melville",
            "year" : "1851",
            "publisher" : "Macmillan",
            "isLent" : False
            }
            ,
            79 : {
            "name" : "Yüzüklerin Efendisi",
            "author" : "J.R.R. Tolkien",
            "year" : "1954",
            "publisher" : "Yapıkredi Yayınları",
            "isLent" : False
            }
        }
        
        self.members = {
            124 : {
            "name" : "Mehmet",
            "phoneNumber" : "0555 555 55 55",
            "email" : "mehmet@yildiz.com",
            "address" : "Ankara",
            "booksLent" : []
            },
            265 : {
            "name" : "Ali",
            "phoneNumber" : "0555 555 55 55",
            "email" : "ali@yildiz.com",
            "address" : "Ankara",
            "booksLent" : []
            }
        }

    def addBook(self):

        book = Book(input("Kitap adı: "),input("Yazar: "),input("Yıl: "),input("Yayınevi: "))
        randomNum = int(random.randint(0,999))
        self.collection[randomNum] = {
            "name" : book.name,
            "author" : book.author,
            "year" : book.year,
            "publisher" : book.publisher,
            "isLent" : False}


        print(f"{book.name} adlı kitap eklendi")
        print(self.collection)


    def removeBook(self,bookID):
        if self.collection[bookID]:
            del self.collection[bookID]
            print(f"{bookID} numaralı kitap silindi")
        else:
            print(f"Hata: {bookID} numaralı Kitap bulunamadı.")

    def addMember(self):
        
        member = Member(input("Ad: "),input("Telefon: "),input("E-posta: "),input("Adres: "))
        randomNum = int(random.randint(0,999))

        self.members[randomNum] = {
            "name" : member.name,
            "phoneNumber" : member.phoneNumber,
            "email" : member.email,
            "address" : member.address,
            "booksLent" : []
        }



    def lendBook(self,MemberID,bookID):
        if self.members[MemberID]:
            if self.collection[bookID]:
                if self.collection[bookID]["isLent"] == False:
                    self.members[MemberID]["booksLent"].append(self.collection[bookID])
                    self.collection[bookID]["isLent"] = True
                    print("Kitap Ödünç verildi")
                else:
                    print("Bu kitap başkasına ödünç verilmiş.")
            else:
                print("Kitap bulunamadı")
        else:
            print(f"{MemberID} numaralı kişinin kaydı bulunamadı.")

    def returnBook(self,MemberID,bookID):
        if bookID in self.collection:
            if MemberID in self.members:
                self.members[MemberID]["booksLent"].remove(self.collection[bookID])
                self.collection[bookID]["isLent"] = False
                print("Kitap iade alındı")
            else:
                print(f"{MemberID} numaralı kişinin kaydı bulunamadı.")
        else:
            print("Kitap bulunamadı")

    def deleteMember(self,MemberID):
        if len(self.members) == 0:
            print("Kayıtlı üye bulunamadı.")
        else:
            if self.members[MemberID]:
                if self.members[MemberID]["booksLent"] == []:
                    del self.members[MemberID]
                    print("Üye silindi.")
                else:
                    print(f"Hata: üye'nin iade etmediği kitap(lar) mevcut.\n {self.members[int(MemberID)]['booksLent']}")
            else:
                print("Bu isimde bir kullanıcı bulunamadı.")

library = Library()

while True:

    Menu = input("\n0-Kitap Listesi\n1-Üye Listesi\n2-Kitap Ekle\n3-Kitap Sil\n4-Üye Ekle\n5-Üye Sil\n6-Kitap Ödünç Ver\n7-Kitap İade Al\n8-Cıkıs\n \nSecim: ")
    print("*"*20)

    if Menu == "0":
        if len(library.collection) == 0:
            print("Kitap kaydı bulunamadı.")
        else:
            for books in library.collection:
                if library.collection[books]["isLent"] == False:
                    print(f"{books} - {library.collection[books]['name']} - {library.collection[books]['author']} - {library.collection[books]['year']} - {library.collection[books]['publisher']} [RAFTA]")
                else:
                    print(f"{books} - {library.collection[books]['name']} - {library.collection[books]['author']} - {library.collection[books]['year']} - {library.collection[books]['publisher']} [ÖDÜNÇ VERİLDİ]")

    elif Menu == "1":
        if len(library.members) == 0:
            print("Üye kaydı bulunamadı.")
        else:
            for members in library.members:
                print(f"No: {members} Üye Adı: {library.members[members]['name']} - Telefon Numarası: {library.members[members]['phoneNumber']} - Email adresi: {library.members[members]['email']} - İkamet Adresi: {library.members[members]['address']}")
                if library.members[members]["booksLent"] != []:
                    print(f"Kitaplar: {library.members[members]['booksLent']}")
    elif Menu == "2":
         library.addBook()
    elif Menu == "3":
         library.removeBook(int(input("Silinecek kitabın numarasını girin: ")))
    elif Menu == "4":
        library.addMember()
    elif Menu == "5":
         library.deleteMember(int(input("Silinecek üyenin numarasını girin: ")))
    elif Menu == "6":
         library.lendBook(int(input("Ödünç verilen üyenin numarasını girin: ")),int(input("Kitabın numarasını girin: ")))
    elif Menu == "7":
        library.returnBook(int(input("İade alınan üyenin numarasını girin: ")),int(input("Kitabın numarasını girin: ")))
    elif Menu == "8":
        print("Programdan çıkılıyor...")
        break
    else:
        print("Hatalı giris.")
