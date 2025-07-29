import java.util.*;

public class assignment {

    // 1. Next Greater Element
    public static List<Integer> nextGreaterElements(int[] arr) {
        Stack<Integer> stack = new Stack<>();
        int n = arr.length;
        Integer[] result = new Integer[n];

        for (int i = n - 1; i >= 0; i--) {
            while (!stack.isEmpty() && stack.peek() <= arr[i]) {
                stack.pop();
            }

            result[i] = stack.isEmpty() ? -1 : stack.peek();
            stack.push(arr[i]);
        }

        return Arrays.asList(result);
    }

    // 2. Array Leaders
    public static List<Integer> arrayLeaders(int[] arr) {
        List<Integer> leaders = new ArrayList<>();
        int n = arr.length;
        int maxFromRight = arr[n - 1];
        leaders.add(maxFromRight);

        for (int i = n - 2; i >= 0; i--) {
            if (arr[i] >= maxFromRight) {
                maxFromRight = arr[i];
                leaders.add(arr[i]);
            }
        }

        // Reverse to maintain original order
        Collections.reverse(leaders);
        return leaders;
    }

    public static void main(String[] args) {
        // Example 1: Next Greater Element
        int[] arr1 = {1, 3, 2, 4};
        System.out.println("Next Greater Elements: " + nextGreaterElements(arr1));

        int[] arr2 = {6, 8, 0, 1, 3};
        System.out.println("Next Greater Elements: " + nextGreaterElements(arr2));

        int[] arr3 = {10, 20, 30, 50};
        System.out.println("Next Greater Elements: " + nextGreaterElements(arr3));

        int[] arr4 = {50, 40, 30, 10};
        System.out.println("Next Greater Elements: " + nextGreaterElements(arr4));

        System.out.println();

        // Example 2: Array Leaders
        int[] arr5 = {16, 17, 4, 3, 5, 2};
        System.out.println("Array Leaders: " + arrayLeaders(arr5));

        int[] arr6 = {10, 4, 2, 4, 1};
        System.out.println("Array Leaders: " + arrayLeaders(arr6));

        int[] arr7 = {5, 10, 20, 40};
        System.out.println("Array Leaders: " + arrayLeaders(arr7));

        int[] arr8 = {30, 10, 10, 5};
        System.out.println("Array Leaders: " + arrayLeaders(arr8));
    }
}
