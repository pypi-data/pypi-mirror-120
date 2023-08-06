from minepy import*
init()
m = Player()
h = ArrayList(Player)
r = String()
while time("Enable"):
    println("started")
while time("Disable"):
    println("finished")
while event("BlockBreakEvent"):
    e = Event("BlockBreakEvent")
    m = e.getPlayer()
    s = Random()
    h = Integer()
    h = s.nextInt(15)+1
    m.setHealth(h)
    r = m.getName()
    m.sendMessage(r)
make()