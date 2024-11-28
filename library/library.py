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
        self.collection = {}
        self.members = {}

    def addBook(self):

        book = Book(input("Kitap adı: "),input("Yazar: "),input("Yıl: "),input("Yayınevi: "))

        self.collection[int((len(self.collection)-1) + 1)] = {
                "name" : book.name,
                "author" : book.author,
                "year" : book.year,
                "publisher" : book.publisher,
                "isLent" : False}


        print(f"{book.name} adlı kitap eklendi")
        print(self.collection)


    def removeBook(self,id):
        if id in self.collection:
            self.collection.remove(self.collection[int(id)])
            print(f"{self.collection[id]['name']} adlı kitap silindi")
        else:
            print(f"Hata: {id} numaralı Kitap bulunamadı.")

    def addMember(self):

        member = Member(input("Ad: "),input("Telefon: "),input("E-posta: "),input("Adres: "))

        self.members[int((len(self.members) - 1) + 1)] = {
            "name" : member.name,
            "phoneNumber" : member.phoneNumber,
            "email" : member.email,
            "address" : member.address,
            "booksLent" : []
        }



    def lendBook(self,MemberID,bookID):
        if self.members[id] in self.members:
            if self.collection[bookID] in self.collection:
                if self.collection[bookID]["isLent"] == False:
                    self.members[MemberID]["booksLent"].append(self.collection[bookID]["name"])
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
                self.members[MemberID]["booksLent"].remove(bookID)
                self.collection[bookID]["isLent"] = False
                print("Kitap iade alındı")
            else:
                print(f"{MemberID} numaralı kişinin kaydı bulunamadı.")
        else:
            print("Kitap bulunamadı")

    def deleteMember(self,name):
        if len(self.members) == 0:
            print("Kayıtlı üye bulunamadı.")
        else:
            print(self.members)
            if name in self.members:
                if self.members[name]["booksLent"] == []:
                    del self.members[name]
                    print("Üye silindi.")
                else:
                    print("Hata: üye'nin iade etmediği kitaplar mevcut.")
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
                print(f"{books} - {library.collection[books]['name']} - {library.collection[books]['author']} - {library.collection[books]['year']} - {library.collection[books]['publisher']}")
    elif Menu == "1":
        if len(library.members) == 0:
            print("Üye kaydı bulunamadı.")
        else:
            for members in library.members:
                print(f"No: {members} Üye Adı: {library.members[members]['name']} - Telefon Numarası: {library.members[members]['phoneNumber']} - Email adresi: {library.members[members]['email']} - İkamet Adresi: {library.members[members]['address']}")
            print(library.members)
    elif Menu == "2":
         library.addBook()
    elif Menu == "3":
         library.removeBook(input("Silinecek kitabın numarasını girin: "))
    elif Menu == "4":
        library.addMember()
    elif Menu == "5":
         library.deleteMember(input("Silinecek üyenin numarasını girin: "))
    elif Menu == "6":
         library.lendBook(int(input("Ödünç verilen üyenin numarasını girin: ")),int(input("Kitabın numarasını girin: ")))
    elif Menu == "7":
        library.returnBook(int(input("İade alınan üyenin numarasını girin: ")),int(input("Kitabın numarasını girin: ")))
    elif Menu == "8":
        print("Programdan çıkılıyor...")
        break
    else:
        print("Hatalı giris.")
