def decimal_to_formatted_hex(decimal_number):
    hex_number = f"{decimal_number:016x}"
    formatted_hex = ":".join(hex_number[i:i+2] for i in range(0, len(hex_number), 2))
    return formatted_hex

class FilterModule(object):
    def filters(self):
        return {
            'decimal_to_formatted_hex': decimal_to_formatted_hex
        }