package com.srib.personaldatabase.service;

import com.srib.personaldatabase.domain.Admin;
import org.springframework.stereotype.Service;
import org.springframework.security.authentication.BadCredentialsException;

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

	private final ECPrivateKey privateKey;
	private final ECPublicKey publicKey;
	private final int expiresIn = 24 * 60 * 60;

	JWTService(ECPublicKey publicKey, ECPrivateKey privateKey) {
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
        	throw new IllegalStateException("Failed to sign token", e);
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
			throw new BadCredentialsException("Token has expired");
		}  catch (UnsupportedJwtException e) {
        	throw new BadCredentialsException("Unsupported token format");
    	} catch (MalformedJwtException e) {
        	throw new BadCredentialsException("Malformed token");
    	} catch (SecurityException e) {
        	throw new BadCredentialsException("Invalid token signature");
    	} catch (IllegalArgumentException e) {
        	throw new BadCredentialsException("Token is null or empty");
		}
	} 


}


