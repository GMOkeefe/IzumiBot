import database as db

async def hello(channel):
  await channel.send("Hello!")

async def pop(user, channel):
  fetch = db.read('pops').where('user_id', user.id).select('pop_num').execute().fetchone()
  pop_num = 0

  if fetch == None:
    pop_num = 0
    db.insert('pops', user_id=user.id, pop_num=1)
    print("not exist")
  else:
    pop_num = fetch[0]
    print("do exist" + str(pop_num))
  pop_num += 1
  await channel.send(str(user.name) + " has popped " + str(pop_num) + " times!")
