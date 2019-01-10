export const setTimeoutPromise = (delay: number) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    },
    delay);
  });
};

// Actionの動的型定義
//
// [参考]
// https://qiita.com/tmnck/items/22cf7df30f7bda5945b3
// https://qiita.com/Takepepe/items/9be98c8a05d22fd08055
type ReturnTypes<Module> = {
  [F in keyof Module]: Module[F] extends (...arg: any[]) => any ?
                   ReturnType<Module[F]> :
                   never;
};

type MapToUnion<T> = T extends {[K in keyof T]: infer U} ? U : never;
export type Action<T> = MapToUnion<ReturnTypes<T>>;
