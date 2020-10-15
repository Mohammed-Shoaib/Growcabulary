import { Injectable } from '@angular/core';
import { join } from '@fireflysemantics/join';
import { Word } from './word.model';

@Injectable({
  providedIn: 'root'
})
export class WordListService {
  words: {};
  basePath: string;
  levels: string[];
  folders: string[];
  wordLists: any[];
  
  constructor() {
    this.basePath = '../../assets';
    this.levels = ['Common', 'Basic', 'Advanced'];
    this.folders = ['Common Words 1', 'Common Words 2', 'Common Words 3', 'Common Words 4', 'Common Words 5', 'Common Words 6', 'Common Words 7', 'Basic Words 1', 'Basic Words 2', 'Basic Words 3', 'Basic Words 4', 'Basic Words 5', 'Basic Words 6', 'Basic Words 7', 'Advanced Words 1', 'Advanced Words 2', 'Advanced Words 3', 'Advanced Words 4', 'Advanced Words 5', 'Advanced Words 6', 'Advanced Words 7'];
  }
  
  ngOnInit() {}
  
  load(): Promise<any> {
    return this.loadWordLists();
  }
  
  async loadWordLists() {
    this.words = {};
    this.wordLists = [];
    for (let i = 0; i < this.folders.length; i++)
      this.wordLists.push(await this.loadWordList(this.folders[i]));
  }
  
  async loadWordList(folder: string) {
    let wordList = [];
    let path = join(this.basePath, folder);
    
    await fetch(join(path, 'data.json'))
    .then(response => response.json())
    .then(words => {
      let keys = Object.keys(words);
      for (let i = 0; i < keys.length; i++) {
        let word: Word;
        for (let value of words[keys[i]])
          if (value['image']) {
            let key = keys[i];
            let audioPath = join(this.basePath, folder, 'audio', key);
            let audio_us = audioPath + '-us.mp3';
            let audio_uk = audioPath + '-uk.mp3';
            let imagePath = join(this.basePath, folder, 'images', value['image']);
            word = new Word(
              key, 
              words[key], 
              value['phonetics-us'][0],
              value['phonetics-uk'][0],
              folder,
              imagePath,
              audio_us,
              audio_uk,
              wordList.length
            );
            break;
          }
        wordList.push(word);
        this.words[keys[i]] = word;
      }
    });
    
    return wordList;
  }
  
  getWord(key: string): Word {
    return this.words[key];
  }
  
  getWordList(folder: string): Word[] {
    let i = this.folders.indexOf(folder);
    for (let j = 0; j < this.wordLists.length; j++)
    if (i === -1) {
      console.log("Not found");   // ! TODO: Handle 404
      return [];
    }
    return this.wordLists[i];
  }
  
  searchQuery(text: string): Word[] {
    let seen = new Set();
    let results: Word[] = [];
    let min_len = Math.min(3, Math.max(1, text.length));
    text = text.toLowerCase();
    
    for (let len = text.length; len >= min_len; len--) {
      let idx = 0;
      let matches: Word[] = [];
      
      for (let wordList of this.wordLists)
        for (let word of wordList)
          if (!seen.has(++idx) && len <= word.key.length && 
              text.substring(0, len) === word.key.substring(0, len).toLowerCase()) {
            matches.push(word);
            seen.add(idx);
          }
      
      matches.sort((a, b) => {
        return a.key.length - b.key.length;
      });
      results = results.concat(matches);
    }
    
    return results;
  }
}