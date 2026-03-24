package com.srib.personaldatabase.service;

import org.springframework.stereotype.Service;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.MalformedJwtException;
import io.jsonwebtoken.UnsupportedJwtException;
import io.jsonwebtoken.security.SecurityException;

import java.security.interfaces.ECPrivateKey;
import java.security.interfaces.ECPublicKey;

import java.util.Date;




@Service
public class JWTService {

	private ECPrivateKey privateKey;
	private ECPublicKey publicKey;
	private int expiresIn = 24 * 60 * 60;

	puclic JWTService(ECPublicKey publicKey, ECPrivateKey privateKey) {
		this.publicKey = publicKey;
		this.privateKey = privateKey;
	}



	// Method creates a JWT token 
	// Signed with the ES256 algorithm
	public String generateToken(Admin admin) {
		if (admin == null || admin.getId() == null) {
			throw new IllegalArgumentException("User or user ID cannot be null");
		}
		
		try {
		String token = Jwts.builder().subject(admin.getId().toString())
			.issuedAt(new Date(System.currentTimeMillis()))
			.expiration(new Date(System.currentTimeMillis() + expiresIn * 1000))
			.signWith(privateKey, Jwts.SIG.ES256).compact();
		return token;
		} catch (SecurityException e) {
        	throw new TokenGenerationException("Failed to sign token", e);
    	}
	}

	public String validateToken(String token) {
		try {
			return Jwts.parser()
				.verifyWith(publicKey)
				.build()
				.parseSignedClaims(token)
				.getPayload()
				.getSubject();
		} catch (ExpiredJwtException e) {
			throw new AuthenticationException("Token has expired");
		}  catch (UnsupportedJwtException e) {
        	throw new AuthenticationException("Unsupported token format");
    	} catch (MalformedJwtException e) {
        	throw new AuthenticationException("Malformed token");
    	} catch (SecurityException e) {
        	throw new AuthenticationException("Invalid token signature");
    	} catch (IllegalArgumentException e) {
        	throw new AuthenticationException("Token is null or empty");
		}
	} 


}


