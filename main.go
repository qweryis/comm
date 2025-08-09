package main

import (
	"crypto/tls"
	"log"
	"net"
	"time"

	"github.com/emersion/go-imap/v2/server"
	"github.com/emersion/go-imap/v2/backend/memory"
)

// A simple in-memory IMAP server backend.
type imapBackend struct {
	*memory.Backend
}

// New creates and initializes the in-memory backend.
func newIMAPBackend() *imapBackend {
	b := memory.New()
	return &imapBackend{
		Backend: b,
	}
}

// Login is called by the server to authenticate a user.
// In this simple example, we accept any username and password.
func (b *imapBackend) Login(conn *server.ConnInfo, username, password string) (*server.Session, error) {
	log.Printf("User %s is logging in...", username)

	// In a real application, you would validate the username and password here.
	// For this example, any credentials are accepted.
	// The in-memory backend will automatically create the user's mailbox.

	return &server.Session{
		Username: username,
		Backend:  b,
	}, nil
}

func main() {
	log.Println("Starting IMAP server...")

	// Create an in-memory backend for the server.
	be := newIMAPBackend()

	// Configure the IMAP server.
	// The Login method on our backend will be used for authentication.
	s := server.New(be)
	s.Addr = ":993" // IMAP over TLS default port
	s.AllowInsecureAuth = true // Allow plain text auth for this example

	// Configure TLS. This is required for secure connections.
	// We'll generate a self-signed certificate for local testing.
	cert, err := tls.X509KeyPair([]byte(certPem), []byte(keyPem))
	if err != nil {
		log.Fatalf("Failed to load TLS key pair: %v", err)
	}
	s.TLSConfig = &tls.Config{
		Certificates: []tls.Certificate{cert},
		// We'll accept any certificate for testing purposes.
		// In a real-world scenario, you would not do this.
		InsecureSkipVerify: true,
	}
	s.ReadTimeout = 10 * time.Minute
	s.WriteTimeout = 10 * time.Minute

	// Create a listener.
	listener, err := net.Listen("tcp", s.Addr)
	if err != nil {
		log.Fatalf("Failed to start listener: %v", err)
	}

	log.Printf("IMAP server listening on %s...", s.Addr)

	// Serve connections.
	if err := s.Serve(listener); err != nil {
		log.Fatalf("Server error: %v", err)
	}
}

// These are self-signed certificate and key for local testing.
// DO NOT use these in a production environment.
const certPem = `
-----BEGIN CERTIFICATE-----
MIICQDCCAaWgAwIBAgIUJ+Ym1Dq5Fj2D4+f3yQ5n3kG4f5swCgYIKoZ... (truncated for brevity)
-----END CERTIFICATE-----
`

const keyPem = `
-----BEGIN PRIVATE KEY-----
MIIEwAIBADANBgkqhkiG9w0BAQEFAASCBKowggSmAgEAAoIBAQC7pQ... (truncated for brevity)
-----END PRIVATE KEY-----
`
