/**
 * Returns a new array containing the elements in arr,
 * with elements at indices grouped together and shifted by offset.
 * Element order is otherwise preserved.
 * 
 * Tip: an offset of -0 groups elements to the left, while +0 groups to the right.
 * 
 * @param {Array} arr The array to reorder.
 * @param {Array} indices The indices of the elements to be repositioned.
 * @param {number} offset The number of positions the elements are to be shifted by.
 * @return {Array} The reordered array.
 */

export function repositioned(arr, indices, offset) {
    if (!Number.isInteger(offset) && offset !== Infinity && offset !== -Infinity) {
        throw new RangeError("The index offset must be an integer or (+/-) Infinity.");
    }

    let isNegativeOffset = (offset < 0) || Object.is(offset, -0);

    let cutoff = isNegativeOffset
        ? Math.min(...indices) + offset
        : Math.max(...indices) + offset + 1;
    
    let leftSlice = [], middleSlice = [], rightSlice = [];

    arr.forEach((element, index) => {
        if (indices.includes(index)) {
            middleSlice.push(element);
        } else if (index < cutoff) {
            leftSlice.push(element);
        } else {
            rightSlice.push(element);
        }
    });

    return [...leftSlice, ...middleSlice, ...rightSlice];
}

/**
 * Returns copy of arr with all elements rotated by offset.
 * arr[i] === rotated(arr)[(i + offset) mod arr.length]
 * 
 * @param {Array} arr The array to be rotated.
 * @param {number} offset The number of positions the elements are to be rotated by.
 * @return {Array} The rotated array.
 */
export function rotated(arr, offset) {
    let cutoff = -offset % arr.length;
    if (cutoff < 0) cutoff += arr.length;
    return [...arr.slice(cutoff), ...arr.slice(0, cutoff)];
}

/**
 * Returns array with all elements in newArr, updated to retain the order 
 * of orderedArr. Elements not present in newArr are removed, and elements
 * not present in orderedArr are appended in the order found in newArr.
 * 
 * @param {Array} orderedArr The original ordered array.
 * @param {Array} newArr The array containing updated elements.
 * @return {Array} The updated array, containing newArr's elements in orderedArr's order.
 */
export function updated(orderedArr, newArr) {
    let count = new Map();
    newArr.forEach((element, index) => {
        let inds = count.get(element);
        if (inds === undefined) {
            inds = [];
            count.set(element, inds);
        }
        inds.push(index);
    });

    let newOrderedArr = [];
    orderedArr.forEach(element => {
        let inds = count.get(element)
        if (inds && inds.length > 0) {
            newOrderedArr.push(element);
            inds.shift();
        }
    });

    let remainingElements = [];
    count.forEach((inds, element) => {
        inds.forEach(i => remainingElements[i] = element);
    });
    newOrderedArr.push(...remainingElements.filter(() => true));

    return newOrderedArr;
}