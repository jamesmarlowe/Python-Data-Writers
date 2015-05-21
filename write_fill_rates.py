import redis
from datawriters.datawriter import DataWriter

r = redis.StrictRedis()
lua = "local time=redis.call(\"TIME\")[1] local stats = {} for i=0,ARGV[1]-1 do     local current = redis.call(\"hgetall\",time-i)     for _, key in pairs(current) do         local sm = redis.call(\"hget\",time-i,key)         stats[key] = (stats[key] or 0) + (sm or 0)     end end local aggregate = {} for k,v in pairs(stats) do     if (not tonumber(k)) then table.insert(aggregate, k..\"=\"..v) end end return aggregate"
stats = r.register_script(lua)

list_values = stats(args=[60])

dict_values = {thing.split("=", 2)[0]:thing.split("=", 2)[1] for thing in list_values}

print dict_values

#DataWriter(writer='mysql', database='data', user='root', table='FillRates').save(data)
