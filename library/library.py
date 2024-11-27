class Library:
    def __init__(self):
        self.collection = {}
        self.members = {}
    
    def addBook(self,book,author):
        if book not in self.collection:
            self.collection.update({
                book : {
                    "author" : author,
                    "isLent" : False
                } 
            })
            print(f"{book} kitabı eklendi")
        else:
            print("Bu kitap zaten mevcut.")
    
    def removeBook(self,book):
        if book in self.collection:
            self.collection.remove(self.collection[book])
            print(f"{book} silindi")
        else:
            print(f"{book} adında bir kitap bulunamadı.")
    
    def addMember(self,name):
        self.members.update({
            name: {
                    "booksLent":[]
            }
        })
    
    def lendBook(self,name,book):
        if name in self.members:
            if book in self.collection:
                if self.collection[book]["isLent"] == False:
                    self.members[name]["booksLent"].append(book)
                    self.collection[book]["isLent"] = True
                    print("Kitap Ödünç verildi")
                else:
                    print("Bu kitap başkasına ödünç verilmiş.")
            else:
                print("Kitap bulunamadı")
        else:
            print(f"{name} adlı kişinin kaydı bulunamadı.")

    def returnBook(self,name,book):
        if book in self.collection and name in self.members:
            self.members[name]["booksLent"].remove(book)
            self.collection[book]["isLent"] = False
            print("Kitap geri alındı")

    def deleteMember(self,name):
        if name in self.members:
            if self.members[name]["booksLent"] == []:
                del self.members[name]
                print("Üye silindi.")
            else: 
                print("Hata: üye'nin iade etmediği kitaplar mevcut.")
        else:
            print("Bu isimde bir kullanıcı bulunamadı.")

library = Library()


