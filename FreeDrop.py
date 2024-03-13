import pygame
import math

# 초기화
pygame.init()

size = [1600, 900]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("자유 낙하")
font = pygame.font.SysFont("consolas", 20)

clock = pygame.time.Clock()
white = (255, 255, 255)
black = (0, 0, 0)
GRAVITY_SCALE = 0.981


class Vector2:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    # 연산자 오버로딩 #
    def __add__(self, other) -> None:  # 덧셈 연산
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, other) -> None:  # 곱셈 연산
        return Vector2(self.x * other.x, self.y * other.y)

    def __eq__(self, __value: object) -> bool:  # 비교 연산
        return self.x == __value.x and self.y == __value.y

    # 연산자 오버로딩 #


# 거리 구하는 메소드
def Distance(pos1: Vector2, pos2: Vector2) -> float:
    return math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)


#


# 각도 구하는 메소드
def GetAngle(pos1: Vector2, pos2: Vector2) -> float:
    return math.atan2(pos2.y - pos1.y, pos2.x - pos1.x) * 180 / math.pi


#


# 화면에 글씨쓰는 메소드
def PrintText(msg, color="BLACK", pos=(50, 50)):
    textSurface = font.render(msg, True, pygame.Color(color), None)
    textRect = textSurface.get_rect()
    textRect.topleft = pos

    screen.blit(textSurface, textRect)


#


# 일반각 구하는 메소드
def GetNormalAngle(angle: float) -> float:
    return (angle % 360 + 360) % 360


#

# def CircleCollision(pos1: Vector2, pos2: Vector2) -> bool:
#     if Distance(pos1, pos2) <= pos1.radius + pos2.radius:
#         return True
#     else:
#         return False


#
class Object:
    def __init__(self) -> None:  # 필드
        self.radius = 40
        self.pos = Vector2(size[0] / 2 - self.radius / 2, size[1] / 2 - self.radius / 2)
        self.mouseDownPos = Vector2(-1, -1)
        self.mouseUpPos = Vector2(-1, -1)
        self.angle = 0
        self.mass = 0.5
        self.velocity = Vector2(0, 0)
        self.gravityScale = 0
        self.isBounded = False

    def Update(self):
        self.gravityScale += GRAVITY_SCALE * self.mass
        if self.pos.y >= size[1] - self.radius:  # 지표면에 닿았을 때
            if self.isBounded == False:  # 튕기기 연산(두 번 튕기게하지 않기 위해)
                self.gravityScale = 0
                self.velocity *= Vector2(0.4, 0.4)
                self.velocity.y = -abs(self.velocity.y)
                self.isBounded = True
            if abs(self.velocity.y) <= 1:
                self.velocity.y = 0

        else:
            self.velocity.y += self.gravityScale
            self.isBounded = False
        if self.pos.y <= self.radius:  # 천장에 닿았을 때
            self.velocity.y = abs(self.velocity.y)
        # self.pos.y += self.gravityScale
        self.pos += self.velocity

    def Render(self):
        # 띄워줄 화면, 선(원) 색깔, 위치좌표, 크기, 선 두께(옵션)

        pygame.draw.circle(screen, black, [self.pos.x, self.pos.y], self.radius, 2)
        if obj.mouseDownPos != Vector2(-1, -1) and obj.mouseUpPos != Vector2(-1, -1):
            pygame.draw.line(
                screen,
                black,
                [obj.mouseDownPos.x, obj.mouseDownPos.y],
                [obj.mouseUpPos.x, obj.mouseUpPos.y],
                3,
            )
        PrintText(
            f"{[obj.mouseDownPos.x, obj.mouseDownPos.y]}, {[obj.mouseUpPos.x, obj.mouseUpPos.y]}, {GetNormalAngle(GetAngle(Vector2(obj.mouseDownPos.x, obj.mouseDownPos.y), Vector2(obj.mouseUpPos.x, obj.mouseUpPos.y)))}"
        )

    def Jump(self):
        self.velocity.y = -30
        self.gravityScale = 0

    def Fire(self, force):
        self.gravityScale = 0
        self.angle = GetAngle(self.mouseDownPos, self.mouseUpPos)
        self.velocity.x += math.cos(self.angle * math.pi / 180) * force
        self.velocity.y += math.sin(self.angle * math.pi / 180) * force
        self.mouseDownPos = Vector2(-1, -1)
        self.mouseUpPos = Vector2(-1, -1)


obj = Object()

end = False

while end == False:
    clock.tick(24)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                obj.Jump()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            obj.mouseDownPos = Vector2(
                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            )
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            obj.mouseUpPos = Vector2(
                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            )
            obj.Fire(Distance(obj.mouseDownPos, obj.mouseUpPos) * 0.1)
        elif event.type == pygame.MOUSEMOTION:
            obj.mouseUpPos = Vector2(
                pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            )

    obj.Update()

    screen.fill(white)
    obj.Render()
    pygame.display.flip()

# 초기화

# --무한반복--
# 업데이트(유저의 입력을 받는 단계)
# 렌더링(그려주기)
# -----------

# 메모리 해제 (릴리즈)

pygame.quit()
