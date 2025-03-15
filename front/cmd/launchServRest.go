package main

import (
	"image/color"
	"log"

	restServ "ia02projetFront/restServer"

)


func main() {

	orientationName := "flat" 
	gridSize := 5
	player1Color := color.RGBA{65, 105, 225, 255} // Bleu
	player2Color := color.RGBA{255, 0, 0, 255}    // Rouge

	const urlserveur = ":8080"

	server := restServ.NewRestServer(urlserveur, orientationName, gridSize, player1Color, player2Color)
	if server == nil {
		log.Fatal("Failed to create the server")
	}

	server.Start()
}