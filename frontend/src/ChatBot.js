import React, { useState, useEffect } from "react";
import io from "socket.io-client";
import {
  Container,
  TextField,
  Button,
  Paper,
  Typography,
  Box,
  Avatar,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import { keyframes } from "@emotion/react";

const socket = io("http://127.0.0.1:5000"); // Conectar con el backend

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const ChatBot = () => {
  const [mensaje, setMensaje] = useState("");
  const [chat, setChat] = useState([]);

  useEffect(() => {
    socket.on("respuesta", (data) => {
      setChat((prevChat) => [
        ...prevChat,
        { usuario: "Bot", mensaje: data.respuesta },
      ]);
    });

    return () => {
      socket.off("respuesta");
    };
  }, []);

  const enviarMensaje = () => {
    if (!mensaje.trim()) return;
    setChat((prevChat) => [...prevChat, { usuario: "Tú", mensaje }]);
    socket.emit("mensaje", { mensaje });
    setMensaje("");
  };

  return (
    <Container
      maxWidth="sm"
      sx={{
        mt: 4,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "90vh",
      }}
    >
      <Paper
        elevation={4}
        sx={{
          p: 3,
          textAlign: "center",
          width: "100%",
          maxWidth: "500px",
          borderRadius: "12px",
          boxShadow: "0px 4px 20px rgba(0, 0, 0, 0.2)",
          background: "linear-gradient(to right, #00b8bf, #000828)",
        }}
      >
        <Typography variant="h5" sx={{ mb: 2, fontWeight: "bold" }}>
          🤖 ChatBot Tienda Inteligente
        </Typography>

        {/* Contenedor de Mensajes */}
        <Box
          sx={{
            border: "2px solid #dee2e6",
            p: 2,
            height: "350px",
            overflowY: "auto",
            backgroundColor: "#ffffff",
            borderRadius: "8px",
            boxShadow: "inset 0px 2px 8px rgba(0, 0, 0, 0.1)",
          }}
        >
          {chat.map((c, i) => (
            <Box
              key={i}
              sx={{
                display: "flex",
                justifyContent: c.usuario === "Tú" ? "flex-end" : "flex-start",
                mb: 1,
                alignItems: "center",
                animation: `${fadeIn} 0.3s ease-in-out`,
              }}
            >
              {c.usuario === "Bot" && (
                <Avatar
                  sx={{
                    bgcolor: "#6c757d",
                    width: 30,
                    height: 30,
                    fontSize: "0.8rem",
                    mr: 1,
                  }}
                >
                  💻​
                </Avatar>
              )}
              <Box
                sx={{
                  p: 1.5,
                  borderRadius: "12px",
                  maxWidth: "75%",
                  backgroundColor: c.usuario === "Tú" ? "#0d6efd" : "#6c757d",
                  color: "#fff",
                  boxShadow: "0px 2px 6px rgba(0, 0, 0, 0.1)",
                  transition: "0.3s ease-in-out",
                }}
              >
                <Typography variant="body2">
                  <strong>{c.usuario}:</strong> {c.mensaje}
                </Typography>
              </Box>
              {c.usuario === "Tú" && (
                <Avatar
                  sx={{
                    bgcolor: "#0d6efd",
                    width: 30,
                    height: 30,
                    fontSize: "0.8rem",
                    ml: 1,
                  }}
                >
                  🧑
                </Avatar>
              )}
            </Box>
          ))}
        </Box>

        {/* Input y Botón de Envío */}
        <Box sx={{ display: "flex", mt: 2, gap: 1 }}>
          <TextField
            fullWidth
            variant="outlined"
            label="Escribe un mensaje..."
            value={mensaje}
            onChange={(e) => setMensaje(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && enviarMensaje()}
            sx={{
              backgroundColor: "#fff",
              borderRadius: "8px",
              boxShadow: "0px 1px 5px rgba(0, 0, 0, 0.1)",
              "& .MuiOutlinedInput-root": {
                "& fieldset": {
                  borderColor: "#dee2e6",
                },
                "&:hover fieldset": {
                  borderColor: "#0d6efd",
                },
                "&.Mui-focused fieldset": {
                  borderColor: "#0d6efd",
                },
              },
            }}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={enviarMensaje}
            sx={{
              minWidth: "50px",
              height: "56px",
              borderRadius: "8px",
              boxShadow: "0px 2px 6px rgba(0, 0, 0, 0.2)",
              "&:hover": {
                backgroundColor: "#0b5ed7",
              },
            }}
          >
            <SendIcon />
          </Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default ChatBot;