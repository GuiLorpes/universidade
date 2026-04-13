package com.guilopes;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        Calculadora calc = new Calculadora();
        System.out.println("=====================================");
        System.out.println("     CALCULADORA DE DOIS FATORES     ");
        System.out.println("=====================================");
        System.out.println("DIGITE A OPERAÇÃO QUE DESEJA REALIZAR");
        System.out.println("DIGITE: x + y = z");
        System.out.println("DIGITE <ENTER> PARA SAIR!");
        String entrada = scan.nextLine();
        // System.out.println(entrada);
        while (entrada != ""){ 
            try {
                String partes[] = entrada.split(" ");
                while (partes.length != 3) {
                    System.out.println("ENTRADA INVÁLIDA!");
                    System.out.println("INSIRA DOIS NÚMEROS E UM OPERADOR\n");
                    System.out.println("DIGITE A OPERAÇÃO QUE DESEJA REALIZAR");
                    entrada = scan.nextLine();
                    partes = entrada.split(" ");
                }

                double n1 = Double.parseDouble(partes[0]);
                double n2 = Double.parseDouble(partes[2]);
                String operador = partes[1];
                calc.setN1(n1);
                calc.setN2(n2);
                double res = 0;
                switch (operador) {
                    case "+":
                        res = calc.somar();
                        break;
                    case "-":
                        res = calc.subtrair();
                        break;
                    case "*":
                        res = calc.multiplicar();
                        break;
                    case "/":
                        res = calc.dividir();
                        break;
                    default:
                        System.out.println("OPERADOR INVALIDO!");
                        break;
                }
                System.out.println("= " + res);

            } catch(ArithmeticException e) {
                System.out.println("Erro: " + e);
            }
            System.out.println("\nDIGITE A OPERAÇÃO QUE DESEJA REALIZAR");
            System.out.println("DIGITE: x + y = z");
            System.out.println("DIGITE <ENTER> PARA SAIR!");
            entrada = scan.nextLine();
        }
        System.out.println("ATÉ A PRÓXIMA! :P");
        System.out.println("=====================================");
        scan.close();
    }
}