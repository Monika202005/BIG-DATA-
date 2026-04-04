from db_connection import get_oltp_connection, get_dw_connection

print("Testing OLTP...")
oltp = get_oltp_connection()

print("Testing DW...")
dw = get_dw_connection()

if oltp:
    print("✅ OLTP Connected!")
    oltp.close()
else:
    print("❌ OLTP Failed")

if dw:
    print("✅ DW Connected!")
    dw.close()
else:
    print("❌ DW Failed")