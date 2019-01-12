import { promisify } from "util";

class MyTimer {
  private timeout: ReturnType<typeof setInterval> | null;

  constructor() {
    this.timeout = null;
  }

  public middleware = () => {
    process.stdout.write("middleware");
    this.start();
  }
  public kill = () => {
    clearInterval(this.timeout!);
  }

  private inc = () => {
    process.stdout.write("inc");
  }

  private start = () => {
    this.timeout = setInterval(this.inc, 500);
  }
}

(async () => {
  const t = new MyTimer();
  t.middleware();
  await promisify(setTimeout)(10000);
  t.kill();
})();
