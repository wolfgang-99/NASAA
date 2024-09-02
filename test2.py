def calculate_percentage(current_amount, stated_amount):
    # Prevent division by zero
    if stated_amount == 0:
        return 100 if current_amount == 0 else 0

    # Calculate the percentage
    percentage = (current_amount / stated_amount) * 100

    # Clamp the percentage between 0 and 100
    return max(0, min(percentage, 100))


# Example usage
current_amount = 100
stated_amount = 2000

percentage = calculate_percentage(current_amount, stated_amount)
print(f"The current amount is {percentage:.2f}% of the stated amount.")
