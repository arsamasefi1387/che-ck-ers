from .constants import SQUARE_SIZE


def get_mouse_square(pos):
    """
    Conversion of mouse pixel coordinates to board grid position.
    
    Args:
        pos (tuple): Mouse position as (x, y) pixel coordinates
    Raises:
        None 
    Returns:
        tuple: Board position as (row, column) 
    """
    x, y = pos
    row = y // SQUARE_SIZE # this is an estimation of where the square is but
    # it is still accurate because it doesn't interfere with other squares
    column = x // SQUARE_SIZE
    return row, column

# This algorithm has been inspired by our teacher Ms.Su!!!
# really really interesting stuff
def mergeSort(alist):
    """
    Sorts list in descending order using merge sort algorithm!
    
    Args:
        alist (list): List of pieces to sort
    Raises:
        None
        
    Returns:
        None: List is sorted in-place
    Note:        
        Comparison uses __gt__ method of pieces to sort kings before pawns.
    """
    if len(alist) > 1:
        mid = len(alist) // 2
        left_half = alist[:mid]
        right_half = alist[mid:]

        # recursion
        mergeSort(left_half)
        mergeSort(right_half)

        left_half_index = 0
        right_half_index = 0
        full_list_index = 0

        while left_half_index < len(left_half) and right_half_index < len(
            right_half
        ):
            if left_half[left_half_index] > right_half[right_half_index]:
                alist[full_list_index] = left_half[left_half_index]
                left_half_index += 1
            else:
                alist[full_list_index] = right_half[right_half_index]
                right_half_index += 1
            full_list_index += 1

        while left_half_index < len(left_half):
            alist[full_list_index] = left_half[left_half_index]
            left_half_index += 1
            full_list_index += 1

        while right_half_index < len(right_half):
            alist[full_list_index] = right_half[right_half_index]
            right_half_index += 1
            full_list_index += 1

