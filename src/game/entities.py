from constants import Orientations
from .base import BaseEntity

class Box(BaseEntity):
    """
    Box class

    Inherited Attributes :
        level (Level object) - The level the box is on
        x (int) - The x coordinate of the box
        y (int) - The y coordinate of the box

    Overriden Properties :
        is_up_available (bool) - True if the box can move up, False otherwise
        is_down_available (bool) - True if the box can move down, False otherwise
        is_left_available (bool) - True if the box can move left, False otherwise
        is_right_available (bool) - True if the box can move right, False otherwise
    
    Properties :
        is_on_goal (bool) - True if the box is on a goal, False otherwise

    Inherited Methods :
        up() - Move the box up
        down() - Move the box down
        left() - Move the box left
        right() - Move the box right

    """
    @property
    def is_up_available(self):
        """
        Check if the box can move up - Override the parent property)

        Returns :
            bool - True if the box can move up, False otherwise
        """
        return super().is_up_available\
            and self.level.get_box(self.x, self.y - 1) is None

    @property
    def is_down_available(self):
        """
        Check if the box can move down - Override the parent property)

        Returns :
            bool - True if the box can move down, False otherwise
        """
        return super().is_down_available\
            and self.level.get_box(self.x, self.y + 1) is None

    @property
    def is_left_available(self):
        """
        Check if the box can move left - Override the parent property)

        Returns :
            bool - True if the box can move left, False otherwise
        """
        return super().is_left_available\
            and self.level.get_box(self.x - 1, self.y) is None

    @property
    def is_right_available(self):
        """
        Check if the box can move right - Override the parent property)

        Returns :
            bool - True if the box can move right, False otherwise
        """
        return super().is_right_available\
            and self.level.get_box(self.x + 1, self.y) is None
    
    @property
    def is_on_goal(self):
        """
        Check if the box is on a goal

        Returns :
            bool - True if the box is on a goal, False otherwise
        """
        return self.level.is_goal(self.x, self.y)


class Player(BaseEntity):
    """
    Player class

    Inherited Attributes :
        level (Level object) - The level the player is on
        x (int) - The x coordinate of the player
        y (int) - The y coordinate of the player

    Attributes :
        orientation (int) - The orientation of the player
        
    Inherited Properties :
        is_up_available (bool) - True if the player can move up, False otherwise
        is_down_available (bool) - True if the player can move down, False otherwise
        is_left_available (bool) - True if the player can move left, False otherwise
        is_right_available (bool) - True if the player can move right, False otherwise
        
    Overriden Methods :
        up() - Move the player up
        down() - Move the player down
        left() - Move the player left
        right() - Move the player right
    """
    PLAYER_NOT_MOVED = 0
    PLAYER_MOVED = 1
    BOX_MOVED = 2
    BOX_ON_GOAL = 3

    def __init__(self, level, x, y, orientation=Orientations.UP):
        super().__init__(level, x, y)
        self.orientation = orientation

    def move(self,
             direction,
             is_available,
             box,
             move_box_available,
             super_move):
        if is_available:
            if box is not None:
                if move_box_available():
                    self.level.save_backup()
                    box.move(direction)
                    super_move()
                    self.orientation = direction
                    if box.is_on_goal:
                        result = self.BOX_ON_GOAL
                    else:
                        result = self.BOX_MOVED
                else:
                    result = self.PLAYER_NOT_MOVED
            else:
                self.level.save_backup()
                super_move()
                self.orientation = direction
                
                result = self.PLAYER_MOVED
        else:
            result = self.PLAYER_NOT_MOVED
        
        if result:
            self.level.add_move()
        return result

    def up(self):
        box = self.level.get_box(self.x, self.y - 1)
        return self.move(
            Orientations.UP, 
            self.is_up_available, 
            box, 
            lambda: box.is_up_available, 
            super().up
        )

    def down(self):
        box = self.level.get_box(self.x, self.y + 1)
        return self.move(
            Orientations.DOWN, 
            self.is_down_available, 
            box, 
            lambda: box.is_down_available, 
            super().down
        )

    def left(self):
        box = self.level.get_box(self.x - 1, self.y)
        return self.move(
            Orientations.LEFT, 
            self.is_left_available, 
            box, 
            lambda: box.is_left_available, 
            super().left
        )

    def right(self):
        box = self.level.get_box(self.x + 1, self.y)
        return self.move(
            Orientations.RIGHT, 
            self.is_right_available, 
            box, 
            lambda: box.is_right_available, 
            super().right
        )
    