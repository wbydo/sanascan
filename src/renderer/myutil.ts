export const setTimeoutPromise = (delay: number) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    },
    delay);
  });
};
