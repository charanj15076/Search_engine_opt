import { Component } from '@angular/core';
import {
  trigger,
  state,
  style,
  animate,
  transition,
} from '@angular/animations';
import { delay } from 'rxjs';

interface Card {
  name: string;
  imageSrc: string;
  linkedinLink: string;
  role: string;
}

@Component({
  selector: 'app-teams-desc',
  templateUrl: './teams-desc.component.html',
  styleUrls: ['./teams-desc.component.css'],
  animations: [
    trigger('cardAnimation', [
      state('visible', style({ opacity: 1, transform: 'scale(1)' })),
      state('hidden', style({ opacity: 0.5, transform: 'scale(0.9)' })),
      transition('visible => hidden', animate('500ms ease-out')),
      transition('hidden => visible', animate('500ms ease-in')),
    ]),
  ],
})
export class TeamsDescComponent {
  cards: Card[] = [
    {
      name: 'Kavil Jain',
      imageSrc: '../../assets/KJ.jpg',
      linkedinLink: 'https://www.linkedin.com/in/kavil-jain-0ab8b7171/',
      role: 'UI Developer',
    },
    {
      name: 'Abhishek Shinde',
      imageSrc: '../../assets/AS.jpg',
      linkedinLink: 'https://www.linkedin.com/in/abhishek-shinde-516259176/',
      role: 'UI Developer',
    },
    {
      name: 'Ken Lester Cue',
      imageSrc: '../../assets/KC.webp',
      linkedinLink: '',
      role: 'Data Engineer',
    },
    {
      name: 'Anurag Ganji',
      imageSrc: '../../assets/AG.jpg',
      linkedinLink: 'https://www.linkedin.com/in/anuragganji/',
      role: 'Project Coordinator',
    },
    {
      name: 'B S Charan Jalukuru',
      imageSrc: '../../assets/CH.jpg',
      linkedinLink: 'https://www.linkedin.com/in/charanjalukuru/',
      role: 'Algorithm Specialist',
    },
    {
      name: 'Suseela Poomdala',
      imageSrc: '../../assets/SS.jpg',
      linkedinLink: '',
      role: 'Visualization Expert',
    },
    {
      name: 'Anirudh Venkatesh',
      imageSrc: '../../assets/AN.jpg',
      linkedinLink: 'https://www.linkedin.com/in/anirudh-venkatesh/',
      role: 'Documentation Lead',
    },
  ];

  cardVisibility = Array(this.cards.length).fill('hidden');
  currentCardIndex = 0;

  toggleCardVisibility(index: number) {
    this.cardVisibility[this.currentCardIndex] = 'hidden';
    this.currentCardIndex = index;
    this.cardVisibility[this.currentCardIndex] = 'visible';
  }

  ngOnInit() {
    setTimeout(() => {
      this.toggleCardVisibility(0);
    }, 500);
    const cardCount = this.cards.length;
    setInterval(() => {
      const nextIndex = (this.currentCardIndex + 1) % cardCount;
      this.toggleCardVisibility(nextIndex);
    }, 2500);
  }

}
