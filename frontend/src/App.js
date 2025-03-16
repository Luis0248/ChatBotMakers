import React from "react";
import ChatBot from "./ChatBot";
import { Box } from "@mui/material";

function App() {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundImage: "url(https://fondosmil.co/fondo/17010.jpg)", // URL de la imagen de fondo
        backgroundSize: "cover", // Ajusta la imagen para cubrir todo el fondo
        backgroundPosition: "center", // Centra la imagen
        backgroundRepeat: "no-repeat", // Evita que la imagen se repita
        padding: "20px",
      }}
    >
      <ChatBot />
    </Box>
  );
}

export default App;