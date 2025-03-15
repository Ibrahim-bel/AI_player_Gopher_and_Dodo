package game

import (
	"log"
	"image/color"

	"github.com/hajimehoshi/ebiten/v2"

	hexgrid "ia02projetFront/game/hexGrid"
	
)

const (
	screenWidth  = 480
	screenHeight = 480
	padding      = 20
)

type Game struct {
	grid    hexgrid.Grid
	Player1 Player
	Player2 Player
}

type Player struct {
	color color.RGBA
}

func (g *Game) Update() error {
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	g.grid.DisplayGrid(screen)
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}

func NewGame(orientationName string, size *hexgrid.Point, origin *hexgrid.Point, player1Color, player2Color color.RGBA, gridRadius int) *Game {
	
	if size == nil {
		size = hexgrid.NewPoint(20.0, 20.0)
	}
	if origin == nil {
		origin = hexgrid.NewPoint(screenWidth/2, screenHeight/2)
	}

	player1 := &Player{
		color: player1Color,
	}

	player2 := &Player{
		color: player2Color,
	}

	grid := hexgrid.NewGrid(orientationName, *size, *origin, gridRadius)

	game := &Game{
		grid:    *grid,
		Player1: *player1,
		Player2: *player2,
	}

	return game
}

func (g *Game)Start(){
	ebiten.SetWindowSize(screenWidth*2, screenHeight*2)
	ebiten.SetWindowTitle("Gohper v1")
	if err := ebiten.RunGame(g); err != nil {
		log.Fatal(err)
	}
}

func (g *Game) Play(player int, x int, y int) error {
    if err := g.grid.AddMove(player, x, y); err != nil {
        return err 
    }
    
    return nil 
}