package hexGrid

import (
	"math"
	"bytes"
	"log"
	"strconv"
	"errors"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
	"github.com/hajimehoshi/ebiten/v2/examples/resources/fonts"
	"github.com/hajimehoshi/ebiten/v2/text/v2"

	"image/color"
)


type tile struct {
	q int
	r int
	s int
	player int 
}

func newTile(q int, r int) *tile {
	t := &tile{q, r, -q - r,0}
	return t
}

func (t tile) GetQ() int {
	return t.q
}

func (t tile) GetR() int {
	return t.r
}

func (t tile) GetS() int {
	return -t.q-t.r
}

func (t tile) IsEmpty() bool {
	if t.player == 0 {
		return true
	}else{
		return false
	}
}

func (t *tile) SetPlayer(player int) {
    t.player = player
}



type orientation struct {
	f0          float64
	f1          float64
	f2          float64
	f3          float64
	b0          float64
	b1          float64
	b2          float64
	b3          float64
	start_angle float64
}

// Fonction pour créer une nouvelle Orientation
func newOrientation(f0, f1, f2, f3, b0, b1, b2, b3, start_angle float64) *orientation {
	orienta := &orientation{f0, f1, f2, f3, b0, b1, b2, b3, start_angle}
	return orienta
}

// constants  orientations
var layoutPointy = orientation{
	f0: math.Sqrt(3.0), f1: math.Sqrt(3.0) / 2.0, f2: 0.0, f3: 3.0 / 2.0,
	b0: math.Sqrt(3.0) / 3.0, b1: -1.0 / 3.0, b2: 0.0, b3: 2.0 / 3.0,
	start_angle: 0.5,
}

var layoutFlat = orientation{
	f0: 3.0/2.0, f1:  -3.0/2.0, f2: -math.Sqrt(3.0)/2.0, f3: -math.Sqrt(3.0) / 2.0,
	b0: 2.0 / 3.0, b1: 0.0, b2: -1.0 / 3.0, b3: math.Sqrt(3.0) / 3.0,
	start_angle: 0.0,
}



type cord struct {
	x int
	y int
}

// Fonction pour créer une nouvelle coordonnées
func newCord(x, y int) *cord {
	cord := &cord{x, y}
	return cord
}



type Point struct {
	x float64
	y float64
}

// Fonction pour créer un nouveau Points
func NewPoint(x, y float64) *Point {
	point := &Point{x, y}
	return point
}



type Grid struct {
	gridOrientation orientation
	size        Point
	origin      Point
	tiles        map[cord]tile
}

// Fonction pour créer une nouvelle Grid
func NewGrid(orientationName string, size Point , origin Point, N int) *Grid {

	var grid Grid
	grid.initTileMap(N)

	switch orientationName {
	case "pointy":
		grid.gridOrientation = layoutPointy
	case "flat":
		grid.gridOrientation = layoutFlat
	default:
		log.Fatalf("Unknown orientation: %s", orientationName)
	}

	grid.size = size
	grid.origin = origin

	return &grid
}

func (g *Grid) initTileMap(N int){
	g.tiles = make(map[cord]tile)

	for q := -N; q <= N; q++ {
		r1 := int(math.Max(float64(-N), float64(q-N)))
		r2 := int(math.Min(float64(N), float64(q+N)))
		for r := r1; r <= r2; r++ {
			g.tiles[*newCord(q, r)] = *newTile(q, r)
		}
	}
}

// Méthode pour convertir une cellule hexagonale en coordonnées pixel
func (g Grid) tileToPixel(t tile) Point {
	M := g.gridOrientation
	x := (M.f0*float64(t.q) + M.f1*float64(t.r)) * g.size.x
	y := (M.f2*float64(t.q) + M.f3*float64(t.r)) * g.size.y
	return *NewPoint(x + g.origin.x, y + g.origin.y)
}

// Méthode pour obtenir le décalage d'un coin hexagonal
func (g Grid) tileCornerOffset(corner int) Point {
	size := g.size
	angle := 2.0 * math.Pi * (float64(g.gridOrientation.start_angle) + float64(corner)) / 6.0
	return *NewPoint(size.x*float64(math.Cos(angle)), size.y*float64(math.Sin(angle)))
}

// Méthode pour obtenir les coins du polygone d'une cellule hexagonale
func (g Grid) polygonCorners(t tile) []Point {
	var corners []Point
	center := g.tileToPixel(t)
	for i := 0; i < 6; i++ {
		offset := g.tileCornerOffset(i)
		corners = append(corners, Point{center.x + offset.x, center.y + offset.y})
	}
	return corners
}

func (g *Grid) IsValidCoordinate(x, y int) bool {
    _, ok := g.tiles[*newCord(x, y)]
    return ok
}

func (g *Grid) AddMove(player int, x, y int) error {
    // Vérifier si les coordonnées sont valides
	coord := newCord(x, y)
    tile, ok := g.tiles[*coord]
    if !ok {
        return errors.New("Coordonnées hexagonales non valides")
    }

    if !g.tiles[*coord].IsEmpty() {
        return errors.New("L'hexagone sélectionné n'est pas vide")
    }

    // Placer le coup du joueur dans cet hexagone
    tile.SetPlayer(player)
    g.tiles[*coord] = tile
    return nil 
}

func (g Grid) DisplayGrid(screen *ebiten.Image) {

	playerColors := map[int]color.RGBA{//a changer
		1: color.RGBA{255, 0, 0, 255},   // Joueur 1 (rouge)
		2: color.RGBA{0, 0, 255, 255},   // Joueur 2 (bleu)
	}

	for _,tile := range g.tiles {
		corners := g.polygonCorners(tile)

		// Convertir les coins en vertex pour DrawTriangles
		vertices := make([]ebiten.Vertex, len(corners))
		for i, corner := range corners {
			vertices[i] = ebiten.Vertex{
				DstX: float32(corner.x),
				DstY: float32(corner.y),
				ColorR: 1, // Rouge
				ColorG: 1,
				ColorB: 1,
				ColorA: 1,
			}
		}
		
		// Créer les indices pour définir les triangles
		indices := make([]uint16, 0, len(vertices)*3)
		for i := 0; i < len(vertices)-1; i++ {
			indices = append(indices, uint16(i), uint16(i+1), uint16(len(vertices)-1))
		}
		indices = append(indices, uint16(len(vertices)-1), uint16(0), uint16(len(vertices)-1))
		
		// Dessiner le polygone plein
		whiteImage := ebiten.NewImage(3, 3)
		whiteImage.Fill(color.White)
		screen.DrawTriangles(vertices, indices,whiteImage, nil)

		//dessiner les contours
		for i := 0; i < len(corners); i++ {
			start := corners[i]
			end := corners[(i+1)%len(corners)]
			ebitenutil.DrawLine(screen, start.x, start.y, end.x, end.y, color.Black)
		}

		// Afficher les coordonnées au centre de l'hexagone
		if tile.IsEmpty() {
			s, err := text.NewGoTextFaceSource(bytes.NewReader(fonts.MPlus1pRegular_ttf))
			if err != nil {
				log.Fatal(err)
			}
			mplusFaceSource := s

			center := g.tileToPixel(tile)
			coord :=  "("+strconv.Itoa(tile.GetQ())+","+strconv.Itoa(tile.GetR())+")"
			op := &text.DrawOptions{}

			op.GeoM.Translate(center.x-10,center.y-5)
			op.ColorScale.ScaleWithColor(color.RGBA{0, 0, 0, 255}) // Black color

			text.Draw(screen, coord, &text.GoTextFace{
				Source: mplusFaceSource,
				Size:   8,
			}, op)
		}else{
			// Dessiner un cercle 
			tileColor := playerColors[tile.player]

			center := g.tileToPixel(tile)
			radius := float64(g.size.x) / 2.0
			ebitenutil.DrawRect(screen, float64(center.x)-radius, float64(center.y)-radius, float64(g.size.x), float64(g.size.y), tileColor)
		}
	}
}

