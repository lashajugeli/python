# import my_module

# print(my_module.COOL_NAME)

n = int(input("ჩაწერეთ ნატურალური რიცხვი:"))

i = 1

m = abs(n)


while i <  m:
    if m == i * i * i:
        if m ==n:
            print(f"კუბური ფესვი არის {i}")
        else:
            print(f"კუბური ფესვი არის {i * -1}")
        break
    else:
        i +=1
if i == m:
    print('ვერ ვიპოვე')