package com.aula09;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        System.out.println("=====================================");
        System.out.println(" Bem vindo ao banco Loirinha Gostosa ");
        System.out.println("=====================================");
        System.out.println("Quais operações deseja realizar?");
        System.out.println("1 - Abrir uma nova conta");
        System.out.println("2 - Verificar saldo");
        System.out.println("3 - Sacar valor");
        System.out.println("4 - Depositar valor");
        System.out.println("5 - Verificar informações da conta");
        System.out.println("0 - Sair");

        int operação = scan.nextInt();
        while ((operação != 0) && (operação < 6)) {
            
        }
        


        scan.close();
    }
}