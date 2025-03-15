package restServer

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"
	"image/color"

	gameT "ia02projetFront/game"
)

type restServer struct {
	sync.Mutex
	addr       string
	game gameT.Game
}




func NewRestServer(addr string, orientationName string, gridSize int, player1Color, player2Color color.RGBA) *restServer {

	gameInstance := gameT.NewGame(
		orientationName,       // Orientation choisie : "pointy" ou "flat"
		nil,                   // Utilise la taille par défaut
		nil,                   // Utilise l'origine par défaut (centre de l'écran)
		player1Color,          // Couleur du joueur 1
		player2Color,          // Couleur du joueur 2
		gridSize,              // Rayon de la grille
	)

	return &restServer{addr: addr, game: *gameInstance}
}

type Position struct {
    X int `json:"x"`
    Y int `json:"y"`
}

type PlayRqst struct {
    Player   int      `json:"Player"`
    Position Position `json:"Position"`
}





func (rsa *restServer) decodePlayRqst(r *http.Request) (req PlayRqst, err error) {
	buf := new(bytes.Buffer)
	buf.ReadFrom(r.Body)
	err = json.Unmarshal(buf.Bytes(), &req)

	return
}

func (rsa *restServer) checkMethod(method string, w http.ResponseWriter, r *http.Request) bool {
	if r.Method != method {
		w.WriteHeader(http.StatusNotImplemented)
		fmt.Fprintf(w, "method %q not implemented", r.Method)
		return false
	}
	return true
}

func (rsa *restServer) handlePlay(w http.ResponseWriter, r *http.Request) {
	rsa.Lock()
	defer rsa.Unlock()

	if !rsa.checkMethod("POST", w, r) {
		return
	}

	req, err := rsa.decodePlayRqst(r)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprint(w, err.Error())
		return
	}
	
	fmt.Printf("Player: %d, Position: (%d, %d)\n", req.Player, req.Position.X, req.Position.Y)
	

	if err := rsa.game.Play(req.Player, req.Position.X, req.Position.Y); err != nil {
        w.WriteHeader(http.StatusInternalServerError)
        fmt.Fprintf(w, "erreur lors de la partie : %v", err)
        return
    }

    // Envoyer un message de réussite si le coup est joué avec succès
    w.WriteHeader(http.StatusOK)
    fmt.Fprint(w, "Coup joué avec succès")
}

func (rsa *restServer) Start() {

	go func() {
		rsa.game.Start()
	}()

	mux := http.NewServeMux()

	mux.HandleFunc("/play", rsa.handlePlay)

	s := &http.Server{
		Addr:           rsa.addr,
		Handler:        mux,
		ReadTimeout:    100 * time.Second,
		WriteTimeout:   100 * time.Second,
		MaxHeaderBytes: 1 << 20}

	log.Println("Listening on", rsa.addr)
	log.Fatal(s.ListenAndServe())
}
