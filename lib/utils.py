# function to be used inside command callback function
from vat_validator.vies import check_vat


def search_VAT(vat, country):

    VAT_info = check_vat(country, vat)
    print("all info extracted-->> " + str(VAT_info))
    if VAT_info.valid:
        return "NAME: " + str(VAT_info.name) + "\n\nADDRESS: " + str(VAT_info.address)
    else:
        return "Invalid response for " + VAT_info.vat + " and country " + VAT_info.country_code


if __name__ == "__main__":
    pass
