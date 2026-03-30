public class Main {
    public static void main(String[] args) {
        Calc calculator = new Calc();
        calculator.setA(43);
        calculator.setB(24);
        int resultado = calculator.soma();
        System.out.println("A soma deu: " + resultado);
    }
}