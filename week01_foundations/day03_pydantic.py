from pydantic import BaseModel

data={"name": "王五", "age": 30, "city": "昆明"}

# 图纸，只声明这一次：字段名 + 应该是什么类型
class User(BaseModel):
    name: str
    age: int
    city: str = "昆明"

u1 = User(name="陈剑", age=21, city="北京")
print(u1.name, u1.age,u1.city)          

u2 = User(name="小李", age="21",city="上海")
print(u2.age, type(u2.age))     

u3 = User(**data)            
print(u3.name, u3.age, u3.city)

u4 = User(name="赵六", age=25)
print( u4.city)  