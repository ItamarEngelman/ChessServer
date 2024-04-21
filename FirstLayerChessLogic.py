from abc import ABC, abstractmethod
import pygame
class Piece():
    """
    מחלקה המייצגת אוביקטים מסוג  חתיכה. לא אמורה לקבל אף משתנה, כי מדובר בעצם במחלקת מעטפת לשאר המחלקות של החתיכות הספציפיות - לא אמורים לייצר אובייקט ממחלקה זו בלבד
    """
    color = None
    image = None
    position = (-1, -1)
    moved = False
    type = None
    @abstractmethod
    def get_possible_moves(self):
        pass
    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def get_moved(self):
        pass

    @abstractmethod
    def get_type(self):
        pass
class Pawn(Piece):
    """
    פעולה המייצגת אוביקטים מסוג פון. יורשת , כמו שאר החתיכות, ממחלקת חתיכה. מקבל את מיקום התמונה, את מיקום החייל והאם הפון זז או לא. הסוג הופך אוטומטית לסוג של פון. כמו כן , מקבל את הצבע של הפון

    """
    def __init__(self, image_path, position, color,  moved = False ):
        #self.image = pygame.image.load(image_path)
        self.position = position
        self.color = color
        self.moved = moved
        self.type = 'Pawn'
    def get_position(self):
        return self.position
    def get_type(self):
        return self.type
    def get_moved(self):
        return self.moved
    def get_possible_moves(self): # פעול המהחזירה את המהלכים האפשריים של הפון במידה ואין הגבלות. מחזיר בשני משתנים נפרדים רשימה שלך מהלכי תזוזה (רגילים) ורשימה של מהלכי אכילה.
        attack_moves = []
        regular_moves = []
        if self.color == 'white':
            offset = 1
        else:
            offset = -1
        attack_moves.extend([(self.position[0] + 1, self.position[1] + offset), (self.position[0] - 1, self.position[1] + offset)])
        regular_moves.append((self.position[0], self.position[1] + offset))
        if self.moved == False:
            regular_moves.append((self.position[0], self.position[1] + 2 * offset))
        return regular_moves, attack_moves
class Bishop(Piece):
    """
       מה שלמטה - רק לרץ
        פעולה המייצגת אוביקטים מסוג פון. יורשת , כמו שאר החתיכות, ממחלקת חתיכה. מקבל את מיקום התמונה, את מיקום החייל והאם הפון זז או לא. הסוג הופך אוטומטית לסוג של פון. כמו כן , מקבל את הצבע של הפון

        """
    def __init__(self, image_path, position, color, moved = False):
        self.image = pygame.image.load(image_path)
        self.position = position
        self.color = color
        self.moved = moved
        self.type = 'Bishop'
    def get_position(self):
        return self.position
    def get_type(self):
        return self.type
    def get_moved(self):
        return self.moved
    def get_possible_moves(self):
        moves_list = []# עובר על כל הדרכים האפשריות ומויסף כל משבצת לפעולות. לא בודק דלום , אפילו לא האם על הלוח
        for i in range(4):  # up-right, up-left, down-right, down-left
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            else:
                x = -1
                y = 1
            while chain < 8:
                moves_list.append((self.position[0] + (chain * x), self.position[1] + (chain * y)))
                chain += 1
        return moves_list
class Rook(Piece):
    """
       מה שלמטה - רק לצריח
        פעולה המייצגת אוביקטים מסוג פון. יורשת , כמו שאר החתיכות, ממחלקת חתיכה. מקבל את מיקום התמונה, את מיקום החייל והאם הפון זז או לא. הסוג הופך אוטומטית לסוג של פון. כמו כן , מקבל את הצבע של הפון

        """
    def __init__(self, image_path, position, color, moved = False):
        #self.image = pygame.image.load(image_path)
        self.position = position
        self.color = color
        self.moved = moved
        self.type = 'Rook'
    def get_position(self):
        return self.position
    def get_type(self):
        return self.type
    def get_moved(self):
        return self.moved
    def get_possible_moves(self):
        moves_list = []
        for i in range(4):  # down, up, right, left
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:

                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            else:
                x = -1
                y = 0
            while chain < 8:
                moves_list.append((self.position[0] + (chain * x), self.position[1] + (chain * y)))
                chain += 1
        return moves_list
class Queen(Piece):
    def __init__(self, image_path, position, color, moved = False):
        #self.image = pygame.image.load(image_path)
        self.position = position
        self.color = color
        self.moved = moved
        self.type = 'Queen'
    def get_position(self):
        return self.position
    def get_type(self):
        return self.type
    def get_moved(self):
        return self.moved
    def get_possible_moves(self):
        moves_list = []
        for i in range(4):  # down, up, right, left
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:

                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            else:
                x = -1
                y = 0
            while chain < 8:
                moves_list.append((self.position[0] + (chain * x), self.position[1] + (chain * y)))
                chain += 1
        for i in range(4):  # up-right, up-left, down-right, down-left
            chain = 1
            if i == 0:
                x = 1
                y = -1
            elif i == 1:
                x = -1
                y = -1
            elif i == 2:
                x = 1
                y = 1
            else:
                x = -1
                y = 1
            while chain < 8:
                moves_list.append((self.position[0] + (chain * x), self.position[1] + (chain * y)))
                chain += 1
        return moves_list
class King(Piece):
    def __init__(self, image_path, position, color, moved = False):
        #self.image = pygame.image.load(image_path)
        self.position = position
        self.color = color
        self.moved = moved
        self.type = 'Queen'
    def get_position(self):
        return self.position
    def get_type(self):
        return self.type
    def get_moved(self):
        return self.moved
    def get_possible_moves(self): #  מחזיר מהלכי המלך רגילים ומהלכי "הצרחה". ההצרחה בודקת רק אם המלך זז  (כי אין לנו מידע נוסף בתוך מחלקה)
        regular_moves = []
        castle_moves = []
        # 8 squares to check for kings, they can go one square any direction
        targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for i in range(8):
            target = (self.position[0] + targets[i][0], self.position[1] + targets[i][1])
            regular_moves.append(target)
        if self.color == 'white':
            offset = 0
        else:
            offset = 7
        if self.moved == False:
            castle_moves.extend([(1, offset), (5, offset)])
        return regular_moves, castle_moves # איבר ראשון שמחזיר הוא המהלכים הרגילים, האיבר שני זה מהלכי הצרחה פוטנציאלים.


king1 = King(0, (3, 0), 'white')
Queen1 = Queen(0, (1, 3), 'white')
Pawn1 = Pawn(0, (1, 3), 'white')
rook1 = Rook(0, (0, 0), 'white')
print(rook1.get_possible_moves())