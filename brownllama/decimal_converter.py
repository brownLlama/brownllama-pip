"""
Decimal Conversion.

This module provides utilities for converting numbers between
English (1,234.56) and German (1.234,56) decimal formats.
"""


class DecimalConverter:
    """
    Converter for English and German number formats.

    Examples:
        - English to German: 1,234.56 -> 1.234,56
        - German to English: 1.234,56 -> 1,234.56

    """

    @staticmethod
    def _format_with_separators(
        number_str: str,
        input_thousands: str,
        input_decimal: str,
        output_thousands: str,
        output_decimal: str,
    ) -> str:
        """
        Convert a number string from one format to another.

        Args:
            number_str: The number string to convert.
            input_thousands: Thousands separator in the input format.
            input_decimal: Decimal separator in the input format.
            output_thousands: Thousands separator for the output format.
            output_decimal: Decimal separator for the output format.

        Returns:
            The formatted number string.

        """
        result = number_str.replace(input_thousands, "").replace(
            input_decimal, output_decimal
        )
        parts = result.split(output_decimal)
        integer_part = parts[0]

        negative = integer_part.startswith("-")
        if negative:
            integer_part = integer_part[1:]

        # Insert thousands separators every 3 digits from the right
        formatted_int = ""
        for i, digit in enumerate(reversed(integer_part)):
            if i > 0 and i % 3 == 0:
                formatted_int = output_thousands + formatted_int
            formatted_int = digit + formatted_int

        if negative:
            formatted_int = "-" + formatted_int

        return (
            f"{formatted_int}{output_decimal}{parts[1]}"
            if len(parts) > 1
            else formatted_int
        )

    @staticmethod
    def english_to_german(number: int | float | str) -> str:
        """
        Convert a number from English to German format.

        Args:
            number: A number as int, float, or English-formatted string.

        Returns:
            The number as a German-formatted string.

        """
        number_str = str(number) if isinstance(number, (int, float)) else number
        return DecimalConverter._format_with_separators(number_str, ",", ".", ".", ",")

    @staticmethod
    def german_to_english(number_str: str) -> str:
        """
        Convert a number from German to English format.

        Args:
            number_str: A number as a German-formatted string.

        Returns:
            The number as an English-formatted string.

        """
        return DecimalConverter._format_with_separators(number_str, ".", ",", ",", ".")
