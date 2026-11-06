PASS [help] memstore add (zh_CN, risk=Low)
PASS [help] memstore add (en_US, risk=Low)
PASS [help] memstore list (zh_CN, risk=Low)
PASS [help] memstore list (en_US, risk=Low)
PASS [help] memstore delete (zh_CN, risk=High)
PASS [help] memstore delete (en_US, risk=High)
PASS [help] memstore disk list (zh_CN, risk=Low)
PASS [help] memstore disk list (en_US, risk=Low)
PASS [help] memstore disk show (zh_CN, risk=Low)
PASS [help] memstore disk show (en_US, risk=Low)
PASS [help] memstore pool create (zh_CN, risk=Low)
PASS [help] memstore pool create (en_US, risk=Low)
PASS [help] memstore pool show (zh_CN, risk=Low)
PASS [help] memstore pool show (en_US, risk=Low)
PASS [help] memstore pool list (zh_CN, risk=Low)
PASS [help] memstore pool list (en_US, risk=Low)
PASS [help] memstore pool delete (zh_CN, risk=High)
PASS [help] memstore pool delete (en_US, risk=High)
PASS [help] memstore namespace create (zh_CN, risk=Low)
PASS [help] memstore namespace create (en_US, risk=Low)
PASS [help] memstore namespace list (zh_CN, risk=Low)
PASS [help] memstore namespace list (en_US, risk=Low)
PASS [help] memstore namespace delete (zh_CN, risk=High)
PASS [help] memstore namespace delete (en_US, risk=High)
PASS [mock] seed list
PASS [mock] seed summary
PASS [mock] add summary
PASS [mock] add FRAME independent
PASS [mock] list filter
PASS [mock] disk list fields
PASS [mock] disk list values
PASS [mock] disk list by storage
PASS [mock] disk show fields
PASS [mock] disk show pools
PASS [mock] pool create split
PASS [mock] pool create response shape
PASS [mock] pool<->disk sync
PASS [mock] pool show
PASS [mock] pool show shape
PASS [mock] pool show demo
PASS [mock] pool list by storage
PASS [mock] pool list demo
PASS [mock] namespace create
PASS [mock] pool used_capacity
PASS [mock] ns list global
PASS [mock] ns list by storage
PASS [mock] ns list by storage filter
PASS [mock] ns list by name
PASS [mock] ns list by pool
PASS [mock] ns pool_name
PASS [mock] negative cases rejected cleanly
PASS [mock] mock file intact after negatives
PASS [mock] ns delete
PASS [mock] pool delete
PASS [mock] disk capacity released
PASS [mock] memstore delete
PASS [mock] mock file valid JSON
PASS [regression] storage list without DME params still rejected
PASS [regression] hci list --help renders
