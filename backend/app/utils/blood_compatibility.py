"""
Blood-type compatibility lookup.

COMPATIBILITY_MAP[X] = list of donor blood groups that CAN donate TO a
patient who needs group X.

Example: COMPATIBILITY_MAP["A+"] -> a patient needing A+ can receive from
O-, O+, A-, or A+ donors.
"""

COMPATIBILITY_MAP: dict[str, list[str]] = {
    "O-": ["O-"],
    "O+": ["O-", "O+"],
    "A-": ["O-", "A-"],
    "A+": ["O-", "O+", "A-", "A+"],
    "B-": ["O-", "B-"],
    "B+": ["O-", "O+", "B-", "B+"],
    "AB-": ["O-", "A-", "B-", "AB-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
}


def get_compatible_donor_groups(needed_blood_group: str) -> list[str]:
    """Returns the list of donor blood groups compatible with the given patient blood group."""
    return COMPATIBILITY_MAP.get(needed_blood_group, [])
