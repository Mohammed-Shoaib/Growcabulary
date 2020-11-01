import { 
  Component, 
  OnInit, 
  Input, 
  Output, 
  EventEmitter, 
  ViewChild, 
  ElementRef, 
  Renderer2, 
  AfterViewInit, 
  OnDestroy 
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { WordListService } from '../word-list.service';
import { Word } from '../word.model';

@Component({
  selector: 'app-word-item',
  templateUrl: './word-item.component.html',
  styleUrls: ['./word-item.component.scss']
})
export class WordItemComponent implements OnInit, AfterViewInit, OnDestroy {
  userText: string;
  startTime: Date; gameStartTime: Date;
  minutes: number; seconds: number;
  wpm: number; accuracy: number;
  totalMinutes: number; totalSeconds: number;
  totalGameMinutes: number; totalGameSeconds: number;
  averageAccuracy: number; prevTotalGameSeconds: number;
  timerInterval: NodeJS.Timer; gameInterval: NodeJS.Timer;
  nextGame: boolean; autoplayAudioUK: boolean; autoplayAudioUS: boolean; keyOnly: boolean;
  dataWPM: number[]; dataAccuracy: number[];
  
  @Input() idx: number;
  @Input() wordList: Word[];
  @Input() readMode: boolean;
  @Output() cardClicked = new EventEmitter<void>();
  @ViewChild('audio_us') audio_us: ElementRef;
  @ViewChild('audio_uk') audio_uk: ElementRef;
  @ViewChild('cardArea') cardArea: ElementRef;
  @ViewChild('textArea') textArea: ElementRef;
  
  constructor(private router: Router,
              private renderer: Renderer2,
              private wordListService: WordListService) {
    // reinitialize values on navigate
    this.router.routeReuseStrategy.shouldReuseRoute = () => false;
    
    // initialize changing values
    this.initialize();
    
    // initialize non-changing values
    this.dataWPM = [0];
    this.dataAccuracy = [100];
    this.autoplayAudioUK = false;
    this.autoplayAudioUS = true;
    this.keyOnly = true;
    this.totalMinutes = this.totalSeconds = 0;
    this.totalGameMinutes = this.totalGameSeconds = this.prevTotalGameSeconds = 0;
  }
  
  ngOnInit() {}

  ngAfterViewInit() {
    if (this.readMode)
      return;
    
    this.textArea.nativeElement.focus();
    this.textArea.nativeElement.value = '';
    this.cardArea.nativeElement.textContent = '';
    
    // add title
    this.addCharacterSpan(this.wordList[this.idx].key, this.cardArea.nativeElement, ['h5'], ['card-title', 'mb-0', 'keep']);
    this.addCharacterSpan('\n', this.cardArea.nativeElement);
    
    // add body
    let values = this.wordList[this.idx].value;
    for (let [i, value] of values.entries()) {
      let div = this.renderer.createElement('div');
      div.classList.add('mt-3');
      
      this.addCharacterSpan(value.pos, div, ['strong', 'em']);
      this.addCharacterSpan('\n' + value.def, div);
      
      if (value.synonyms.length) {
        this.addCharacterSpan('\n', div);
        this.addCharacterSpan('synonyms: ', div, ['strong']);
        this.addCharacterSpan(value.synonyms.join(', '), div);
      }
      if (value.antonyms.length) {
        this.addCharacterSpan('\n', div);
        this.addCharacterSpan('antonyms: ', div, ['strong']);
        this.addCharacterSpan(value.antonyms.join(', '), div);
      }
      if (value.notes) {
        this.addCharacterSpan('\n', div);
        this.addCharacterSpan('Notes: ', div, ['strong']);
        this.addCharacterSpan(value.notes, div);
      }
      if (i + 1 < values.length)
        this.addCharacterSpan('\n', div);
      else
        div.classList.add('mb-5');
      
      this.cardArea.nativeElement.appendChild(div);
    }
    
    // calculate performance
    this.evaluate();
  }
  
  ngOnDestroy() {
    clearInterval(this.timerInterval);
    clearInterval(this.gameInterval);
  }
  
  initialize() {
    // initialize variables
    this.startTime = undefined;
    this.accuracy = 100;
    this.minutes = this.seconds = this.wpm = 0;
    this.userText = '';
    this.nextGame = false;
  }
  
  resetState() {
    clearInterval(this.timerInterval);
    this.initialize();
    this.ngAfterViewInit();
  }
  
  addCharacterSpan(text: string, parent, tagNames: string[] = [], className?: string[]) {
    text.split('').forEach(character => {
      let span = this.renderer.createElement('span');
      let prev = span;
      
      for (let tagName of tagNames) {
        let tag = this.renderer.createElement(tagName);
        prev.appendChild(tag);
        prev = tag;
      }
      
      if (character === '\n')
        character = '↵' + '\n';
      if (className) {
        span.classList.add(...className);
        prev.classList.add(...className); // ! Don't really like the double adding being done here
      }
      
      prev.innerText = character;
      parent.appendChild(span);
    });
  }
  
  evaluate() {
    let cardSpans = [];
    let incorrectCount = 0;
    
    [...this.cardArea.nativeElement.children].forEach((tag) => {
      let classId = 'keep';
      if (tag.tagName === 'SPAN') {
        if (!this.keyOnly || this.keyOnly && tag.className.includes(classId))
          cardSpans.push(tag);
        return;
      }
      for (let child of tag.children)
        if (child.tagName === 'SPAN')
          if (!this.keyOnly || this.keyOnly && child.className.includes(classId))
            cardSpans.push(child);
    });
    
    cardSpans.forEach((characterSpan, index) => {
      let value = characterSpan.innerText;
      const character = this.userText[index];
      if (value === '↵\n')
        value = '\n';
      if (character == null) {
        characterSpan.classList.remove('correct');
        characterSpan.classList.remove('incorrect');
      } else if (character === value) {
        characterSpan.classList.remove('incorrect')
        characterSpan.classList.add('correct');
      } else {
        incorrectCount++;
        characterSpan.classList.remove('correct');
        characterSpan.classList.add('incorrect');
      }
      
      let prev = characterSpan;
      for (let tag of characterSpan.children) {
        if (tag.tagName === 'BR')
          break;
        prev = tag;
      }
      prev.classList.remove('current');
      if (index === this.userText.length)
        prev.classList.add('current');
    });
  
    // calculate WPM
    let characterCount = cardSpans.length;
    let count = Math.max(0, (this.userText.length - 2 * incorrectCount) / 5);
    let minutes = this.minutes + this.seconds / 60;
    if (minutes)
      this.wpm = Math.round(count / minutes);
    this.accuracy = 100 * (characterCount - incorrectCount) / characterCount;
    
    if (characterCount === this.userText.length) {
      this.nextGame = true;
      this.dataWPM.push(this.wpm);
      this.dataAccuracy.push(this.accuracy);
      clearInterval(this.timerInterval);
      this.prevTotalGameSeconds += this.minutes * 60 + this.seconds;
    }
  }
  
  updateTimer() {
    let milliseconds = new Date().valueOf() - this.startTime.valueOf();
    this.seconds = Math.floor(milliseconds / 1000) % 60;
    this.minutes = Math.floor(milliseconds / (1000 * 60));
    
    let totalTime = this.prevTotalGameSeconds + this.minutes * 60 + this.seconds;
    this.totalGameMinutes = Math.floor(totalTime / 60);
    this.totalGameSeconds = totalTime % 60;
    
    this.evaluate();
  }
  
  getAverage(data) {
    if (data.length === 1)
      return data[0];
    let values = data.slice(1);
    const sum = values.reduce((a, b) => a + b, 0);
    return sum / values.length;
  }
  
  getCorrect(data) {
    return [...data].filter(x => x === 100).length;
  }
  
  onCardClick() {
    if (this.readMode)
      this.cardClicked.emit();
  }
  
  onAudioClickUS() {
    this.audio_us.nativeElement.play();
  }
  
  onAudioClickUK() {
    this.audio_uk.nativeElement.play();
  }
  
  toggleAutoplayAudio() {
    this.autoplayAudioUK = !this.autoplayAudioUK;
  }
  
  toggleKeyOnly() {
    this.keyOnly = !this.keyOnly;
  }
  
  leftArrowClick() {
    this.idx = Math.max(0, this.idx - 1);
    this.resetState();
  }
  
  rightArrowClick() {
    if (this.idx === this.wordList.length - 1) {
      let folder = this.wordList[this.idx].folderName;
      let folders = this.wordListService.folders;
      let index = folders.indexOf(folder);
      let nextFolder = folders[(index + 1) % folders.length];
      this.router.navigate(['/learn', nextFolder]);
      return;
    }
    this.idx = Math.min(this.wordList.length - 1, this.idx + 1);
    this.resetState();
  }
  
  onTextChange(userText: string, lastKey: string) {
    if (this.nextGame) {
      if (lastKey === null)
        this.rightArrowClick();
      return;
    }
    if (!this.startTime) {
      this.startTime = new Date();
      this.timerInterval = setInterval(() => this.updateTimer(), 1000);
    }
    if (!this.gameStartTime) {
      this.gameStartTime = new Date();
      this.gameInterval = setInterval(() => {
        let milliseconds = new Date().valueOf() - this.gameStartTime.valueOf();
        this.totalSeconds = Math.floor(milliseconds / 1000) % 60;
        this.totalMinutes = Math.floor(milliseconds / (1000 * 60));
      }, 1000);
    }
    
    this.userText = userText.trimLeft();
    this.userText = this.userText.replace(/ +/g, ' ');
    this.userText = this.userText.replace(/\s*\n+\s*/g, '\n');
    
    this.evaluate();
    
    this.textArea.nativeElement.value = this.userText;
  }
}