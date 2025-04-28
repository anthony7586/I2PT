## this file appends to a destination file

from datetime import datetime

def approve_part(current_user):
  
    comment_line_seperator = "\n\n################################################\n################################################\n\n"
    # Open the source file in read mode
    with open("qr_data.txt", "r") as source_file:
        # Read the source contents of the file
        source_contents = source_file.read()


    # Open the destination file in append mode
    with open("approved_parts.txt", "r") as destination_file:
        destination_contents = destination_file.read()
        # Append the source contents to the destination file


   

    with open("approved_parts.txt", "a") as destination_file:

        if len(destination_contents) == 0:
            if len(source_contents) > 0:
                destination_file.write("\n" + current_user + "\n" +str(datetime.now()) + "\n" + source_contents)
        else:
            if len(source_contents) > 0:
                destination_file.write(comment_line_seperator)
                destination_file.write(current_user + "\n" + str(datetime.now()) + "\n\n" + source_contents)


    # Open the source file again in write mode to erase the source contents
    with open("qr_data.txt", "w") as source_file:
        # Writing nothing to the source file erases its contents
        source_file.write("")


    print("Contents successfully appended to approved_parts.txt and qr_data.txt has been cleared.")


if __name__ == "__main__":
    approve_part()