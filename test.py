
from ContentStore import ContentStore
from Name import Name
from Data import Data
from Keys import Keys
from IDS import IDS


key = Keys()
private_key = key.get_private_key()
public_key = key.get_public_key()

ids = IDS()
name = "/"+str(public_key)+"/"
data = Data(name, "test")
cs = ContentStore()
cs.add(Name(name),data)
print(cs.get())
print(cs.get_data_by_name(name))

