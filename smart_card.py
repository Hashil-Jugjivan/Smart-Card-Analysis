import re
from smartcard.System import readers
from smartcard.util import toHexString

# MIFARE Ultralight commands
CMD_GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
CMD_READ_BLOCK = [0xFF, 0xB0, 0x00, 0x04, 0x04]
CMD_GET_TRANSACTION_LOG = None

# Function to send APDU commands to the card
def send_apdu(connection, apdu_cmd):
   data, sw1, sw2 = connection.transmit(apdu_cmd)
   response = toHexString(data)
   status_code = "SW1: {:02X}, SW2: {:02X}".format(sw1, sw2)
   return response, status_code

def main():
   # Get all available smart card readers
   card_readers = readers()

   if not card_readers:
       print("No smart card readers found.")
       return
   print("Available smart card readers:")
   for reader in card_readers:
       print(reader)

   # Select the reader you want to connect to....
   reader = card_readers[1]
   # Connect to the selected reader
   connection = reader.createConnection()
   connection.connect()
   # Send command to get UID
   response, status_code = send_apdu(connection, CMD_GET_UID)

   if status_code == "SW1: 90, SW2: 00":
       # Extract UID from the response
       uid = response[:]
       print("Response:", uid)
   else:
       print("Failed to retrieve UID.")

   # READ BALANCE
   CMD_READ_BALANCE = [0x90, 0x32, 0x03, 0x00, 0x00]
   response, status_code = send_apdu(connection, CMD_READ_BALANCE)

   # print(response)
   card_value = response[6:15]
   print(card_value)
   card_balance_string = card_value.split()
   new_value = card_balance_string[0] + card_balance_string[1] + card_balance_string[2]

   # print(new_value)
   new_new_value = "0x" + new_value
   decimal = (int(new_new_value, 16)) / 100
   print("Balance = $" + str(decimal))
   print("")

   # READ TRANSACTION LOG
   CMD_TRANSACTION_LOG = [0x90, 0x32, 0x03, 0x00, 0x01, 0x00, 0x00]
   response, status_code = send_apdu(connection, CMD_TRANSACTION_LOG)

   # print(response)
   transaction_data_string = response.split()
   chunk_size = 16
   transactions = []
   for i in range(0, len(transaction_data_string), 16):
       transaction = transaction_data_string[i:i+16]
       transactions.append(transaction)
   # print(transactions)
   for i in transactions:
       transaction_type = i[0]
       transaction_amount = i[1:4]
       # print(transaction_amount)

       if transaction_type == "75":
           print("Offline Value Add")
           transaction_amount_combined = transaction_amount[0] + transaction_amount[1] + transaction_amount[2]
           transaction_amount_hex_string = "0x" + transaction_amount_combined
           decimal = (int(transaction_amount_hex_string, 16)) / 100
           print("Amount = $" + str(decimal))

       elif transaction_type == "76":
           print("Bus Refund")
           transaction_amount_combined = transaction_amount[0] + transaction_amount[1] + transaction_amount[2]
           transaction_amount_hex_string = "0x" + transaction_amount_combined
           decimal = (int(transaction_amount_hex_string, 16)) / 100
           print("Amount = $" + str(decimal))

       elif transaction_type == "31":
           print("Bus Payment")
           transaction_amount_combined = transaction_amount[0] + transaction_amount[1] + transaction_amount[2]
           transaction_amount_string = "" + transaction_amount_combined
           num = int(transaction_amount_string, 16)
           bit_length = len(transaction_amount_string) * 4
           mask = (1 << bit_length) - 1
           twocomp = ((~num) & mask) + 1
           result = format(twocomp, f'0{len(transaction_amount_string)}X')
           decimal = (int(result, 16)) / 100
           print("Amount = $" + str(decimal))

       elif transaction_type == "30":
           print("MRT Payment")
           transaction_amount_combined = transaction_amount[0] + transaction_amount[1] + transaction_amount[2]
           transaction_amount_string = "" + transaction_amount_combined
           num = int(transaction_amount_string, 16)
           bit_length = len(transaction_amount_string) * 4
           mask = (1 << bit_length) - 1
           twocomp = ((~num) & mask) + 1
           result = format(twocomp, f'0{len(transaction_amount_string)}X')
           decimal = (int(result, 16)) / 100
           print("Amount = $" + str(decimal))

       transaction_datetime = i[4:8]
       print("Date: ", transaction_datetime)
       transaction_userdata = i[8:17]
       text = []
       for i in transaction_userdata:
           character_string = "" + i
           new_data = bytes.fromhex(character_string)
           ascii_text = new_data.decode('ascii')
           text.append(ascii_text)
       final_string = ''.join(text)
       print(final_string)
       text = []
       # print(transaction_userdata)
       print()

   # Disconnect from the reader
   connection.disconnect()
   
if __name__ == "__main__":
   main()
