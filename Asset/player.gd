extends Node2D

var player_position = Vector2(200, 200)
var player_size = Vector2(100, 100)
var speed = 200

func _process(delta):
	var velocity = Vector2.ZERO

	if Input.is_action_pressed("ui_right"):
		velocity.x += 1
	if Input.is_action_pressed("ui_left"):
		velocity.x -= 1
	if Input.is_action_pressed("ui_down"):
		velocity.y += 1
	if Input.is_action_pressed("ui_up"):
		velocity.y -= 1

	player_position += velocity.normalized() * speed * delta
	queue_redraw()

func _draw():
	draw_rect(Rect2(player_position, player_size), Color.RED)
