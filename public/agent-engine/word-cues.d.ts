declare module "*.json" {
  const value: Array<{
    word: string;
    startFrame: number;
    endFrame: number;
    scene: string;
  }>;
  export default value;
}
