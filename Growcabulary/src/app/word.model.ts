export class Word {
  constructor(
    public key: string, 
    public value: any, 
    public phonetic_us: string,
    public phonetic_uk: string, 
    public folderName: string,
    public imagePath: string,
    public audio_us: string,
    public audio_uk: string,
    public index: number) {}
}